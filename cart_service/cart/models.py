import uuid

from django.db import models


class CartItemManager(models.Manager):
    def get_queryset(self):
        return super(CartItemManager, self).get_queryset().filter(is_active=True)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        abstract = True


class Cart(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class CartItem(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    prod_id = models.CharField(max_length=100)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = CartItemManager()

    def sub_total(self, prod_price):
        return prod_price * self.quantity


class ItemOptions(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='item_options')
    attribute = models.CharField(max_length=60)
    value = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
