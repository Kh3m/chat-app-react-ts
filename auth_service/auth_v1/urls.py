from django.urls import path, re_path, include
from auth_v1.views import Evaluate_request
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('', Evaluate_request.as_view(), name='evaluate_request'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api-docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
