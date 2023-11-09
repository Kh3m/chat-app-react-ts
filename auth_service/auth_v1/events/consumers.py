import json
import threading
from django.core.cache import cache

from .utils.rbmq import RBMQ
from .event_handlers import handle_user_logged_out

rbmq_client = RBMQ(exchange_name="auth_service_exchange",
                   exchange_type="direct")


def consume_events():
    while True:
        rbmq_client.consume_event(
            "user_service_exchange",
            "user_logged_out",
            handle_user_logged_out
        )

        # ...consume more events


consumer_thread = threading.Thread(target=consume_events)
consumer_thread.daemon = True
consumer_thread.start()
