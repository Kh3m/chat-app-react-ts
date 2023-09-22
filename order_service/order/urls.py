from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('orders', views.OrderViewSet, basename='orders')

urlpatterns = [
    path('orders/user/<int:user_id>', views.UserOrderHistoryView.as_view(), name="order.history"),
    path('orders/<uuid:pk>', views.UpdateOrders.as_view(), name="order.update"),
    path('orders/<uuid:order_id>/orderitems', views.OrderItemsView.as_view(), name="order.order_items.view"),
    path('orders/<uuid:order_id>/orderitems/create', views.CreateOrderItemView.as_view(),
         name="order.order_items.create"),
    path('orders/<uuid:order_id>/orderitems/<uuid:order_item_id>', views.OrderItemsView.as_view(),
         name="order.order_items.modify"),
]

urlpatterns += router.urls
