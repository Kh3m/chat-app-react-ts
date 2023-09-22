from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from api_v1.views import *

actions = {
    'get': 'retrieve',
    'put': 'update',
    'post': 'create',
    'patch': 'partial_update',
    'delete': 'destroy'
}

api_root = {}

product_detail = ProductsViewSet.as_view(actions)
product_list = ProductsViewSet.as_view({'get': 'list', 'post': 'create'})

category_detail = CategoryViewSet.as_view(actions)
category_list = CategoryViewSet.as_view({'get': 'list', 'post': 'create'})

# urlpatterns = [
#     path('products/', product_list, name='product-list'),
#     path('products/<str:pk>/', product_detail, name='product-detail'),
#     path('products/categories/', category_list, name='category-list'),
#     path('products/categories/<str:pk>/',
#          category_detail, name='category-detail'),

# ]

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename="product")
router.register(r'categories', CategoryViewSet, basename="category")
router.register(r'reviews', ReviewsViewSet, basename="review")
router.register(r'variants', VariantsViewSet, basename="variant")
router.register(r'options', OptionsViewSet, basename="option")
router.register(r'images', ImagesViewSet, basename="image")

urlpatterns = [
    path('', include(router.urls)),
]
