from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


from api_v1.views import *


router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename="product")
router.register(r'categories', CategoryViewSet, basename="category")
router.register(r'reviews', ReviewsViewSet, basename="review")
router.register(r'variants', VariantsViewSet, basename="variant")
router.register(r'options', OptionsViewSet, basename="option")
router.register(r'images', ImagesViewSet, basename="image")

urlpatterns = [
    path('', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]
