import pika
import json
from pika.exchange_type import ExchangeType

# Establish a connection to the RabbitMQ server
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

# Declare an exchange for user-related events
channel.exchange_declare(
    exchange='user_service_exchange', exchange_type=ExchangeType.direct)


def publish_new_registration(user_data, key):
    message = {"user": user_data, "key": key}
    channel.basic_publish(
        exchange="user_service_exchange",
        routing_key="new_registration",
        body=json.dumps(message)
    )


def publish_password_reset(token, uidb64):
    message = {"token": token, "uidb64": uidb64}
    channel.basic_publish(
        exchange="user_service_exchange",
        routing_key="password_reset",
        body=json.dumps(message)
    )


def publish_user_logged_out():
    pass
