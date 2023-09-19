from django.db import models
from django_ulid.models import default, ULIDField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey


class Category(models.Model):
    """Represents a category for products."""
    id = ULIDField(default=default, primary_key=True)
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.name


class Image(models.Model):
    """Represents an image associated with a product or variant."""
    id = ULIDField(default=default, primary_key=True)
    url = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = ULIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"Image URL for {self.content_object}: {self.url}"

    class Meta:
        indexes = [models.Index(fields=["content_type", "object_id"]),]


class Product(models.Model):
    """Represents a product."""
    id = ULIDField(default=default, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    user_id = models.CharField(max_length=30)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False)
    images = GenericRelation(Image)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Represents a review for a product."""
    id = ULIDField(default=default, primary_key=True)
    user_id = models.CharField(max_length=30)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.body[:50]


class Variant(models.Model):
    """Represents a variant of a product."""
    id = ULIDField(default=default, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Option(models.Model):
    """Represents an option or attribute of a product's variation."""
    id = ULIDField(default=default, primary_key=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    value = models.CharField(max_length=30, unique=True)
    price = price = models.DecimalField(max_digits=15, decimal_places=2)
    images = GenericRelation(Image)

    def __str__(self):
        return self.value
