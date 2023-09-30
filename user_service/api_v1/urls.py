from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib.auth.views import LoginView, LogoutView

from api_v1.views import UserViewSet, ProfileViewSet, AddressViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename="user")
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'Adresses', AddressViewSet, basename="address")

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
