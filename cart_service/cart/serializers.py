import logging

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Cart, CartItem, ItemOptions
from .utils import get_existing_cart_item, merge_cart_items, set_guest_cart_id

logger = logging.getLogger(__name__)


class ItemOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOptions
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


class CartItemSerializer(serializers.ModelSerializer):
    item_options = ItemOptionsSerializer(many=True, required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'prod_id', 'item_options', 'quantity', 'is_active', 'created_at', 'modified_at']

        unique_together = ['prod_id', 'item_options']

    def create(self, validated_data):
        cart_id = self.context['cart_id']
        logger.info(f"cart_id {cart_id} context received in CartItemSerializer")
        cart = get_object_or_404(Cart, id=cart_id)  # Remove options from validated_data
        item_options_data = validated_data.pop('item_options', [])  # Change field name to match the model

        existing_cart_item = get_existing_cart_item(cart, validated_data['prod_id'], item_options_data)
        logger.info(f'get_existing_cart_item function returned {existing_cart_item}')

        if existing_cart_item:
            merge_cart_items(existing_cart_item, validated_data['quantity'])
            cart_item = existing_cart_item
        else:
            cart_item = CartItem(cart=cart, **validated_data)
            cart_item.save()  # Save the cart item to generate an ID

            # Create and associate ItemOptions instances
            for option_data in item_options_data:
                ItemOptions.objects.create(cart_item=cart_item, **option_data)

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
        fields = ['id', 'cart', 'prod_id', 'quantity', 'is_active']
