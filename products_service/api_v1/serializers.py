import logging
from .models import *
from rest_framework import serializers


logger = logging.getLogger("api_v1")


class BaseSerializer(serializers.HyperlinkedModelSerializer):
    """Base serializer with logging functionality"""
    id = serializers.UUIDField(read_only=True)

    def create(self, validated_data):
        class_name = self.__class__.__name__
        try:
            logger.info(f'{class_name} - Object created successfully.')
            return super().create(validated_data)
        except Exception as e:
            logger.error(f'{class_name} - Failed to create object: {str(e)}')
            raise serializers.ValidationError(
                f"{class_name} - Failed to create object: {str(e)}")


class ProductSerializer(BaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", format="html")

    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(BaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="category-detail", format="html")

    class Meta:
        model = Category
        fields = "__all__"

    subcategories = serializers.SerializerMethodField()

    def get_subcategories(self, instance):
        try:
            subcategories_count = Category.objects.filter(
                parent=instance.id).count()
            return subcategories_count
        except Exception as e:
            logger.error(f"Failed to get subcategories: {str(e)}")
            return 0


class ReviewSerializer(BaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="review-detail", format="html")

    class Meta:
        model = Review
        fields = "__all__"


class VariantSerializer(BaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="variant-detail", format="html")

    class Meta:
        model = Variant
        fields = "__all__"


class ImageSerializer(BaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="image-detail", format="html")

    class Meta:
        model = Image
        fields = ['url', 'id', 'image_url', 'object_id']


class OptionSerializer(BaseSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="option-detail", format="html")

    images = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = "__all__"

    def get_images(self, instance):
        try:
            images = instance.images.all()
            image_serializer = ImageSerializer(images, many=True)
            return image_serializer.data
        except Exception as e:
            logger.error(f"Failed to get images for option: {str(e)}")
            return []
