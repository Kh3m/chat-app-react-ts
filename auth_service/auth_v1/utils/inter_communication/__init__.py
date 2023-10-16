"""Registers functions that communicate with other microservices."""

from .user_service import get_user_cert

communicate = {
    #'micro-service': {'communication functions'}
    'users': {'get_user_cert': get_user_cert},
}