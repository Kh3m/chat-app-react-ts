import logging

from rest_framework import serializers
from .models import Order, OrderItem

# Define a logger for this module
logger = logging.getLogger(__name__)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'delivery_address_id', 'order_status', 'delivery_charge', 'is_payment_successful']

    def save(self, **kwargs):
        order_items = self.validated_data.pop('order_items', [])

        # Create the order instance without saving it yet
        order = Order.objects.create(**self.validated_data)
        total_price = sum([item.item_price for item in order_items]) + self.validated_data['delivery_charge']
        order.order_total_price = total_price
        order.save()

        # add a logging statement
        logger.info(f"Order {order.id} created successfully")
        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'order_status', 'cancel_order']


class InlineOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'order_status']


class OrderItemSerializer(serializers.ModelSerializer):
    order = InlineOrderSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'variation_ids', 'product_id', 'item_price', 'quantity', 'is_item_ordered']


class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'variation_ids', 'product_id', 'item_price', 'quantity', 'is_item_ordered']

    def create(self, validated_data):
        order_id = self.context['order_id']

        try:
            # check whether the order_id in the url params exists
            order = Order.objects.only('id').get(id=order_id)
        except Order.DoesNotExist:
            # Handle the case where the order does not exist
            logger.error(f"Order with id={order_id} does not exist")
            raise ValueError("Order with id={} does not exist".format(order_id))

        logger.info(f"OrderItem created for Order {order.id}")
        return OrderItem.objects.create(order_id=order.id, **validated_data)


