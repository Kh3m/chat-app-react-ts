import logging
from django.dispatch import receiver
from allauth.account.signals import (
    user_signed_up, email_confirmation_sent,
    password_reset, email_confirmed, user_logged_in,
    user_logged_out
)

from api_v1.events import publishers
from api_v1.serializers import UserSerializer

logger = logging.getLogger("api_v1_events")


@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    serializer = UserSerializer(user, context={'request': request})
    user_data = serializer.data
    publishers.publish_user_signed_up(user_data)


@receiver(email_confirmation_sent)
def handle_email_confirmation_sent(request, confirmation, signup, **kwargs):
    email, key = str(confirmation.email_address), confirmation.key
    publishers.publish_email_confirmation(email, key)


@receiver(email_confirmed)
def handle_email_confirmed(request, email_address, **kwargs):
    publishers.publish_email_confirmed(str(email_address))


@receiver(password_reset)
def handle_password_set(request, user, **kwargs):
    serializer = UserSerializer(user, context={'request': request})
    user_data = serializer.data


@receiver(user_logged_in)
def handle_user_logged_in(request, user, **kwargs):
    print("User logged in!")
    serializer = UserSerializer(user, context={'request': request})
    user_data = serializer.data
    publishers.publish_user_logged_in(user_data)


@receiver(user_logged_out)
def handle_user_logged_out(request, user, **kwargs):
    data = {
        "user_id": str(user.id),
        "auth_token": str(request.auth)
    }
    print(data)
    publishers.publish_user_logged_out(data)
