import time
import logging
from django.core.cache import cache

logger = logging.getLogger("auth_v1")


class RateLimiter:
    def __init__(self, settings):
        self.settings = settings

    def get_rate_limit(self, user_groups):
        rate_limit = self.settings['default']
        for rank in reversed(self.settings.keys()):
            if rank in user_groups:
                rate_limit = self.settings[rank]
                break
        return rate_limit

    def allow(self, user_id, user_groups):
        rate_limit = self.get_rate_limit(user_groups)
        if rate_limit:
            allowed_requests, time_frame = rate_limit.split('/')
            time_frame = time_frame.lower()
            user_key = f"rate_limit:{user_id}"

            if time_frame == 's':
                time_window = 1
            elif time_frame == 'm':
                time_window = 60
            elif time_frame == 'h':
                time_window = 3600
            else:
                logger.error(f"Unsupported time frame {time_frame}")
                raise ValueError(f"Unsupported time frame: {time_frame}")

        current_time = time.time()
        request_list = cache.get(user_key, [])

        while request_list and (current_time - request_list[0][0]) > time_window:
            request_list.pop(0)

        if len(request_list) < int(allowed_requests):
            request_list.append((current_time, 1))
            cache.set(user_key, request_list, time_window)

            return True

        return False
