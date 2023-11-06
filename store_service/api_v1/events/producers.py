from .utils.rbmq import RBMQ

# Establish a connection to the RabbitMQ server
rbmq_client = RBMQ(exchange_name="store_service_exchange",
                   exchange_type="direct")


def publish_member_invite(store_id, email_address):
    routing_key = "member_invite"
    message = {"store_id": store_id, "email": email_address}
    rbmq_client.publish_event(message, routing_key)
