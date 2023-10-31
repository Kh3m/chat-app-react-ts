import json
import logging
import redis
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Cart, CartItem, ItemOption
from .utils import get_existing_cart_item_redis, merge_cart_items, set_guest_cart_id

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

logger = logging.getLogger(__name__)


class ItemOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOption
        fields = ['id', 'attribute', 'value']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'created_at', 'modified_at']
        extra_kwargs = {'user_id': {'required': False}}

    def create(self, validated_data):
        cart = Cart.objects.create(**validated_data)
        set_guest_cart_id(cart.id)
        # log new cart creation
        logger.info("New cart created successfully")
        return cart


class CartItemRetrievalSerializer(serializers.ModelSerializer):
    item_options = ItemOptionsSerializer(many=True, required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'prod_id', 'item_options', 'quantity', 'is_active', 'created_at', 'modified_at']


class CartItemQuantityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'created_at', 'modified_at']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value


class CartItemSerializer(serializers.ModelSerializer):
    item_options = ItemOptionsSerializer(many=True, required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'prod_id', 'item_options', 'quantity', 'is_active', 'created_at', 'modified_at']

        unique_together = ['prod_id', 'item_options']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

    def create(self, validated_data):
        cart_id = self.context['cart_id']
        redis_key = f'cart:main:{cart_id}'

        cart_data_json = redis_client.get(redis_key)
        cart = json.loads(cart_data_json.decode('utf-8'))
        # if cart is None:
        #     cart = get_object_or_404(Cart, id=cart_id)

        logger.info(f"cart_id {cart_id} context received in CartItemSerializer")

        # Remove options from validated_data
        item_options_data = validated_data.pop('item_options', [])

        existing_cart_item = get_existing_cart_item_redis(cart, validated_data['prod_id'], item_options_data)
        logger.info(f'get_existing_cart_item function returned {existing_cart_item}')

        if existing_cart_item:
            print('EXISTING CART ITEM AVAILABLE')
            merge_cart_items(cart, existing_cart_item, validated_data['quantity'])
            cart_item = existing_cart_item
        else:
            logger.warning(f'No cart item with {item_options_data} found')
            print(f'No cart item with {item_options_data} found')
            cart_item = CartItem(cart_id=cart['id'], **validated_data)
            cart_item.save()  # Save the cart item to generate an ID

            # Create and associate ItemOptions instances
            for option_data in item_options_data:
                ItemOption.objects.create(cart_item=cart_item, **option_data)

        # Log the creation or merge of a cart item
        logger.info(f"Cart with ID {cart_id} retrieved")
        return cart_item


class RetrieveCartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'cart_items', 'created_at', 'modified_at']


class CustomCartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True, required=False)
    item_options = ItemOptionsSerializer(many=True, required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'item_options', 'prod_id', 'quantity', 'is_active']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value


class CustomItemOptionsSerializer(serializers.ModelSerializer):
    cart_item = CustomCartItemSerializer(read_only=True)
    class Meta:
        model = ItemOption
        fields = ['id', 'cart_item', 'attribute', 'value', 'created_at']