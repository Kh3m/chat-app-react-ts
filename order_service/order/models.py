from django.contrib.postgres.fields import ArrayField
from django.db import models
import uuid


class OrderManager(models.Manager):
    def get_queryset(self):
        return super(OrderManager, self).get_queryset().filter(is_payment_successful=True)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Order(TimeStampedModel):
    STATUS = (
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=50)
    delivery_address_id = models.CharField(max_length=50)
    order_status = models.CharField(max_length=15, choices=STATUS, default="Pending")
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2)
    order_total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    cancel_order = models.BooleanField(default=False)
    is_payment_successful = models.BooleanField(default=False)

    objects = OrderManager()

    class Meta:
        db_table = "orders"


class OrderItem(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    variation_ids = ArrayField(models.CharField(max_length=36), null=True)
    product_id = models.CharField(max_length=50)
    item_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_item_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'order_items'



