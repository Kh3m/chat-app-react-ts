import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Order, OrderItem
from .pagination import DefaultPagination
from .serializers import (
    OrderSerializer,
    OrderItemSerializer,
    OrderUpdateSerializer,
    CreateOrderItemSerializer,
)

# Define a logger for this module
logger = logging.getLogger(__name__)


class OrderViewSet(ModelViewSet):
    """
    Viewset for managing orders.

    This viewset allows you to create, retrieve, update, and delete orders.
    """
    http_method_names = ['get', 'post', 'head', 'options', 'delete']
    serializer_class = OrderSerializer
    pagination_class = DefaultPagination
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        # Log the creation of a new order
        logger.info(f"Order created by user with ID {request.user.id}")
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Log the deletion of an order
        logger.info(f"Order deleted with ID {kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)


class OrderItemsView(generics.ListAPIView):
    """
    API view for listing order items.

    This view returns a list of items associated with a specific order.
    """
    serializer_class = OrderItemSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        logger.info(f"Order items retrieved for order with ID {order_id}")

        return OrderItem.objects.filter(order_id=order_id)


class UpdateOrdersView(generics.UpdateAPIView):
    """
    API view for updating orders.

    This view allows you to partially update order details: the order_status .
    """
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer

    def update(self, request, *args, **kwargs):
        # Log the update of an order
        logger.info(f"Order updated with ID {kwargs['pk']}")
        return super().update(request, *args, **kwargs)


class UserOrderHistoryView(generics.ListAPIView):
    """
    API view for retrieving user order history.

    This view returns a list of orders associated with a specific user.
    """
    serializer_class = OrderSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        # log the retrieval of user order history
        logger.info(f"User order history retrieved for user with ID {user_id}")
        return Order.objects.filter(user_id=user_id)


class CreateOrderItemView(generics.CreateAPIView):
    """
    API view for creating order items.

    This view allows you to add new items to an existing order.
    """
    serializer_class = CreateOrderItemSerializer
    queryset = OrderItem.objects.all()

    def get_serializer_context(self):
        return {'order_id': self.kwargs['order_id']}

    def create(self, request, *args, **kwargs):
        # log the creation of a new order item
        logger.info("Order item created for order with ID %s", kwargs['order_id'])
        return super().create(request, *args, **kwargs)


class RetrieveOrderItemView(generics.RetrieveAPIView):
    """
    API view for retrieving and updating order items.

    This view allows you to retrieve and update details of individual order items.
    """
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def retrieve(self, request, *args, **kwargs):
        order_id = Order.objects.only('id').get(id=self.kwargs['order_id']).id
        logger.info(f"Order with ID {kwargs['order_id']} retrieved successfully")
        instance = OrderItem.objects.get(order_id=order_id, id=self.kwargs['order_item_id'])
        logger.info(f"Order item with ID {kwargs['order_item_id']}")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
