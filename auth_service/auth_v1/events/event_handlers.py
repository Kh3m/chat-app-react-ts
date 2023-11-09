import json
import logging
from django.core.cache import cache

logger = logging.getLogger("auth_v1")


def handle_user_logged_out(channel, method, properites, body):
    """Handles user's logout event"""
    user_data = json.loads(body)
    auth_token = user_data['auth_token']

    cache_key = auth_token.split('.')[-1] \
        if '.' in auth_token else auth_token[8]
    cache.set(cache_key, {})

    channel.basic_ack(delivery_tag=method.delivery_tag)
    logger.info('Successfully consumed "user_logged_out" event')
