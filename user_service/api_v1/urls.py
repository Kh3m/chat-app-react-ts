from django.urls import path, re_path, include
from allauth.socialaccount.views import signup
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api_v1.views import UserViewSet, ProfileViewSet, AddressViewSet
from api_v1.views import GoogleLogin, Generate_user_cert


router = DefaultRouter()
router.register(r'users', UserViewSet, basename="user")
router.register(r'users/profiles', ProfileViewSet, basename='profile')
router.register(r'users/adresses', AddressViewSet, basename="address")

urlpatterns = [
    path('users/auth/', include('dj_rest_auth.urls')),
    path('users/auth/registration/', include('dj_rest_auth.registration.urls')),
    path("signup/", signup, name="socialaccount_signup"),
    path('users/auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('users/auth/cert/', Generate_user_cert.as_view(), name='user_cert'),
    path('users/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('users/api-docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include(router.urls)),
]
