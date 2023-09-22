from api_v1.models import Category, Image, Product, Review, Variant, Option
from api_v1.utils import is_valid_ulid
from api_v1.serializers import *

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError


class ProductsViewSet(viewsets.ModelViewSet):
    """Manage products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'], url_path='reviews')
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='variants')
    def variants(self, request, pk=None):
        product = self.get_object()
        variants = product.variants.all()

        response_data = []

        for variant in variants:
            options = Option.objects.filter(variant=variant)
            option_serializer = OptionSerializer(options, many=True)

            variant_data = {
                "id": str(variant.id),
                "name": variant.name,
                "options": option_serializer.data
            }
            response_data.append(variant_data)

        return Response(response_data, status=status.HTTP_200_OK)


class ReviewsViewSet(viewsets.ModelViewSet):
    """Manage reviews"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Manage categories"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        parent_param = self.request.query_params.get('parent', None)

        if parent_param is not None:
            parent_param = parent_param.lower()

        if parent_param == 'null' or parent_param == 'none':
            return Category.objects.filter(parent=None)
        elif parent_param:
            if is_valid_ulid(parent_param):
                return Category.objects.filter(parent=parent_param)
            else:
                return Category.objects.none()
        else:
            return Category.objects.all()


class VariantsViewSet(viewsets.ModelViewSet):
    """Manage variants"""
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer


class OptionsViewSet(viewsets.ModelViewSet):
    """Manage options"""
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class ImagesViewSet(viewsets.ModelViewSet):
    """Manage images"""
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
