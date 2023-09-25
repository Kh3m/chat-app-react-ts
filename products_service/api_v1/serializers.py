from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", format="html")
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="category-detail", format="html")
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"

    subcategories = serializers.SerializerMethodField()

    def get_subcategories(self, instance):
        subcategories_count = Category.objects.filter(
            parent=instance.id).count()
        return subcategories_count


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="review-detail", format="html")
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class VariantSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="variant-detail", format="html")
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Variant
        fields = "__all__"


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="image-detail", format="html")

    class Meta:
        model = Image
        fields = ['url', 'id', 'image_url', 'object_id']


class OptionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="option-detail", format="html")

    images = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = "__all__"

    def get_images(self, instance):
        images = instance.images.all()
        image_serializer = ImageSerializer(images, many=True)
        return image_serializer.data
