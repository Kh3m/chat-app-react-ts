from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api_v1.views import StoreViewSet, MemberViewSet, SocialViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet, basename='store')
router.register(r'members', MemberViewSet, basename='member')
router.register(r'socials', SocialViewSet, basename='social')

urlpatterns = [
    path('', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
