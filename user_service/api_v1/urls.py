from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api_v1.views import UserViewSet, ProfileViewSet, AddressViewSet
from api_v1.views import GoogleLogin

router = DefaultRouter()
router.register(r'users', UserViewSet, basename="user")
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'Adresses', AddressViewSet, basename="address")

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
