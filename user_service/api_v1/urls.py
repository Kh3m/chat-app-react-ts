from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from dj_rest_auth.registration.views import (
    ResendEmailVerificationView,
    VerifyEmailView,
    RegisterView
)
from dj_rest_auth.views import (
    PasswordResetConfirmView,
    PasswordResetView,
    LoginView,
    LogoutView,
    UserDetailsView,
)

from api_v1.views import UserViewSet, ProfileViewSet, AddressViewSet
from api_v1.views import GoogleLogin, Generate_user_cert
from api_v1.views import email_confirm_redirect, password_reset_confirm_redirect


router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'adresses', AddressViewSet, basename="address")
router.register(r'', UserViewSet, basename="user")

# urlpatterns = [
#     path("auth/user/", UserDetailsView.as_view(), name="rest_user_details"),
#     path("auth/register/", RegisterView.as_view(), name="rest_register"),
#     path("auth/register/verify-email/", VerifyEmailView.as_view(),
#          name="rest_verify_email"),
#     path("auth/register/resend-email/", ResendEmailVerificationView.as_view(),
#          name="rest_resend_email"),
#     path("auth/login/", LoginView.as_view(), name="rest_login"),
#     path("auth/logout/", LogoutView.as_view(), name="rest_logout"),
#     path("auth/account-confirm-email/<str:key>/",
#          email_confirm_redirect, name="account_confirm_email"),
#     path("auth/account-confirm-email/", VerifyEmailView.as_view(),
#          name="account_email_verification_sent"),
#     path("auth/password/reset/", PasswordResetView.as_view(),
#          name="rest_password_reset"),
#     path(
#         "auth/password/reset/confirm/<str:uidb64>/<str:token>/",
#         password_reset_confirm_redirect,
#         name="password_reset_confirm",
#     ),
#     path("auth/password/reset/confirm/", PasswordResetConfirmView.as_view(),
#          name="password_reset_confirm"),

#     path('auth/google/', GoogleLogin.as_view(), name='google_login'),
#     path('auth/cert/', Generate_user_cert.as_view(), name='user_cert'),
#     path('schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('api-docs/',
#          SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     path('', include(router.urls)),
# ]

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/cert/', Generate_user_cert.as_view(), name='user_cert'),
    path(
        "auth/password/reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_confirm_redirect,
        name="password_reset_confirm",
    ),
    path("auth/account-confirm-email/<str:key>/",
         email_confirm_redirect, name="account_confirm_email"),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', include(router.urls)),
]
