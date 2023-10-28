from django.urls import path, re_path, include
from allauth.socialaccount.views import signup
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api_v1.views import UserViewSet, ProfileViewSet, AddressViewSet
from api_v1.views import GoogleLogin, Generate_user_cert


router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'adresses', AddressViewSet, basename="address")
router.register(r'', UserViewSet, basename="user")

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path("signup/", signup, name="socialaccount_signup"),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/cert/', Generate_user_cert.as_view(), name='user_cert'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include(router.urls)),
]
