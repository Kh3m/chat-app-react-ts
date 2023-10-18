from django.urls import path, re_path, include
from auth_v1.views import Evaluate_request

urlpatterns = [
    path('', Evaluate_request.as_view(), name='evaluate_request'),
]
