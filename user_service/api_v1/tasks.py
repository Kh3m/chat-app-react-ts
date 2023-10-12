import os
import django
import jwt
from api_v1.models import User
from django.conf import settings
from celery import shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_service.settings')
settings.configure()
django.setup()


@shared_task
def generate_certificate(auth_token):
    """Generates user certificate"""
    print('++++++++++=================++++++++++++++')
    from rest_framework_simplejwt.tokens import Token

    try:
        decoded_token = decode_handler(auth_token)
        user_id = decoded_token['user_id']
        user = User.objects.get(id=user_id)

        certificate = {
            'user_id': user.id,
            'expiration': decoded_token['exp'],
            'groups': user.groups.all(),
            'permissions': user.get_all_permissions()
        }

        return ('OK', certificate)
    except jwt.ExpiredSignatureError:
        return ('ERROR', 'Expired token')
    except jwt.InvalidTokenError:
        return ('Error', 'Invalid token')
    except User.DoesNotExist:
        return ('Error', "User doesn't exist")


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk2OTUyNTEwLCJpYXQiOjE2OTY5NTA3MTAsImp0aSI6ImY2ZjE2N2Y3YTZkMjRhNjA5ZDBjOTNkMDZlY2I4M2FhIiwidXNlcl9pZCI6IjY1NGEwY2JkLWQ4YmEtNGM0OC1hMDI0LWI3MDQyZjc5MTUzNyJ9.em5e4qGhnHpnwynU5m1HtqM2qdhAcj-2WmDehHI5v6o"
response = generate_certificate(token)
