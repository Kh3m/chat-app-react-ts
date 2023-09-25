import uuid
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey


class Category(models.Model):
    """Represents a category for products."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.name

    def __repr__(self):
        obj = vars(self)
        obj['id'] = str(self.id)
        return str(obj)


class Image(models.Model):
    """Represents an image associated with a product or variant."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_url = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"Image URL for {self.content_object}: {self.url}"

    def __repr__(self):
        obj = vars(self)
        obj['id'] = str(self.id)
        return str(obj)

    class Meta:
        indexes = [models.Index(fields=["content_type", "object_id"]),]


class Product(models.Model):
    """Represents a product."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    user_id = models.CharField(max_length=30)
    reviews = models.ManyToManyField(
        "Review", related_name="products_reviews", null=True)
    variants = models.ManyToManyField(
        "Variant", related_name="products_variants", null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False)
    images = GenericRelation(Image)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.name

    def __repr__(self):
        obj = vars(self)
        obj['id'] = str(self.id)
        return str(obj)


class Review(models.Model):
    """Represents a review for a product"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=30)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_reviews")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.body[:50]

    def __repr__(self):
        obj = vars(self)
        obj['id'] = str(self.id)
        return str(obj)


class Variant(models.Model):
    """Represents a variant for one or more products"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    products = models.ManyToManyField(
        "Product", related_name="products_variants", null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        obj = vars(self)
        obj['id'] = str(self.id)
        return str(obj)


class Option(models.Model):
    """Represents an option or attribute of a product's variation"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(max_length=30, unique=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    images = GenericRelation(Image)

    def __str__(self):
        return self.value

    def __repr__(self):
        obj = vars(self)
        obj['id'] = str(self.id)
        return str(obj)
