import logging
from .utils.rbmq import RBMQ

logger = logging.getLogger("api_v1_events")

# Establish a connection to the RabbitMQ server
rbmq_client = RBMQ(exchange_name="user_service_exchange",
                   exchange_type="direct")


def publish_user_signed_up(user_data):
    routing_key = "user_signed_up"
    message = {"user": user_data}
    rbmq_client.publish_event(message, routing_key)


def publish_user_logged_in(user_data):
    routing_key = "user_logged_in"
    message = {"user": user_data}
    rbmq_client.publish_event(message, routing_key)


def publish_user_logged_out(user_id, auth_token):
    routing_key = "user_logged_out"
    message = {"user_id": user_id, "auth_token": auth_token}
    rbmq_client.publish_event(message, routing_key)


def publish_email_confirmation(email, key):
    routing_key = "email_confirmation"
    message = {"email": email, "key": key}
    rbmq_client.publish_event(message, routing_key)


def publish_email_confirmed(email):
    routing_key = "email_confirmed"
    message = {"email": email}
    rbmq_client.publish_event(message, routing_key)


def publish_password_reset(email, token, uidb64):
    routing_key = "password_reset"
    message = {"user_email": email, "token": token, "uidb64": uidb64}
    rbmq_client.publish_event(message, routing_key)
