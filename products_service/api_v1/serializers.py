import json
from rest_framework import serializers
from .models import *
from api_v1.utils import serialize_ULID
from django_ulid.models import ULIDField
from ulid import ULID


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = serialize_ULID(representation)
        return representation


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    def get_subcategories(self, instance):
        subcategories = Category.objects.filter(parent=instance.id)
        serializer = CategorySerializer(subcategories, many=True)
        return len(serializer.data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = serialize_ULID(representation)
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = serialize_ULID(representation)
        return representation


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = serialize_ULID(representation)
        return representation


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class OptionSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = "__all__"

    def get_images(self, instance):
        images = instance.images.all()
        image_serializer = ImageSerializer(images, many=True)
        return image_serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation = serialize_ULID(representation)
        return representation
