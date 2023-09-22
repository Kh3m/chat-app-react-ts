from django.contrib import admin
from .models import Order, OrderItem


class OrdersModel(admin.ModelAdmin):
    list_display = ('order_status', 'user_id', 'delivery_address_id', 'delivery_charge', 'cancel_order', 'created_at')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('delivery_address_id',)


class OrderItemsModel(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_id', 'item_price', 'quantity', 'is_item_ordered', 'modified_at')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('item_price',)


admin.site.register(Order, OrdersModel)
admin.site.register(OrderItem, OrderItemsModel)
