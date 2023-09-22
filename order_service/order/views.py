from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from .models import Order, OrderItem
from .pagination import DefaultPagination
from .serializers import (OrderSerializer,
                          OrderItemSerializer, OrderUpdateSerializer, CreateOrderItemSerializer,
                          )


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options', 'delete']
    serializer_class = OrderSerializer
    pagination_class = DefaultPagination
    queryset = Order.objects.all()


class UpdateOrders(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer


class UserOrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(user_id=user_id)


class CreateOrderItemView(generics.CreateAPIView):
    serializer_class = CreateOrderItemSerializer
    queryset = OrderItem.objects.all()

    def get_serializer_context(self):
        return {'order_id': self.kwargs['order_id']}


class RetrieveUpdateOrderItemView(generics.CreateAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def get_serializer_context(self):
        return {'order_id': self.kwargs['order_id']}


class OrderItemsView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return OrderItem.objects.filter(order_id=order_id)
