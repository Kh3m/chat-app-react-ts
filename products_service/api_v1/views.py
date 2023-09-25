from api_v1.models import Category, Image, Product, Review, Variant, Option
from api_v1.serializers import *

import logging
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from django.core.exceptions import ValidationError


logger = logging.getLogger('api_v1')


class ProductsViewSet(viewsets.ModelViewSet):
    """Manage products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'], url_path='reviews')
    def reviews(self, request, pk=None):
        try:
            product = self.get_object()
            reviews = product.reviews.all()
            serializer = ReviewSerializer(
                reviews, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Failed to retrieve reviews: {str(e)}")
            return Response({"error": "Failed to retrieve reviews."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], url_path='variants')
    def variants(self, request, pk=None):
        try:
            product = self.get_object()
            variants = product.variants.all()

            response_data = []

            for variant in variants:
                options = Option.objects.filter(variant=variant)
                option_serializer = OptionSerializer(
                    options, many=True, context={'request': request})

                variant_data = {
                    "id": str(variant.id),
                    "name": variant.name,
                    "options": option_serializer.data
                }
                response_data.append(variant_data)

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Failed to retrieve variants: {str(e)}")
            return Response({"error": "Failed to retrieve variants."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewsViewSet(viewsets.ModelViewSet):
    """Manage reviews"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Manage categories"""
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'], url_path='subcategories')
    def subcategories(self, request, pk=None):
        try:
            category = self.get_object()

            categories = Category.objects.filter(parent=category)
            category_serializer = CategorySerializer(
                categories, many=True, context={'request': request})

            return Response(category_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Failed to retrieve subcategories: {str(e)}")
            return Response({"error": "Failed to retrieve subcategories."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        try:
            parent_param = self.request.query_params.get('parent', None)

            if parent_param is not None:
                parent_param = parent_param.lower()

            if parent_param == 'null' or parent_param == 'none':
                return Category.objects.filter(parent=None)
            elif parent_param:
                try:
                    return Category.objects.filter(parent=parent_param)
                except ValueError:  # invalid UUID
                    return Category.objects.none()
            else:
                return Category.objects.all()
        except Exception as e:
            logger.error(f"Failed to retrieve categories: {str(e)}")
            return Response({"error": "Failed to retrieve categories."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

    def perform_create(self, serializer):
        try:
            object_id = self.request.data.get('object_id')
            model_class = Product.objects.filter(
                id=object_id) or Option.objects.filter(id=object_id)

            if not model_class:
                raise NotFound("Object does not exist")

            content_type = ContentType.objects.get_for_model(model_class[0])
            serializer.save(content_type=content_type, object_id=object_id)
        except NotFound as e:
            logger.error(str(e))
            return Response({"error": "Object does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Failed to create image: {str(e)}")
            return Response({"error": "Failed to create image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
