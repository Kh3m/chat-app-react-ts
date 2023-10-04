import os
import dotenv
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

dotenv.load_dotenv()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('review.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

# Configuration for the development mode
if os.getenv('DEBUG'):
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls))),
