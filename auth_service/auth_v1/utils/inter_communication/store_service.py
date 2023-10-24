"""Defines functions that communicate with the Store Service"""
import logging
import requests

logger = logging.getLogger("auth_v1")


def check_membership(store_id, user_id):
    """
    Returns True is a user is a member of a specific store,
    False otherwise.
    """
    url = f"http://localhost:8003/api/v1/stores/{store_id}/"
    response = requests.get(url=url)

    if response.status_code != 200:
        logger.error({
            'message': f"Failed to check membership for store {store_id}",
            'error': response.content
        })
        return False

    store_info = response.json()
    return user_id in store_info.members


def check_ownership(store_id, user_id):
    """
    Returns True is a user is the owner of a specific store,
    False otherwise.
    """
    url = f"http://localhost:8000/api/v1/stores/{store_id}/"
    response = requests.get(url=url)

    if response.status_code != 200:
        logger.error({
            'message': f"Failed to verify ownership with Store Service",
            'detail': f"Error {response.status_code} - {response.json()['error']}"
        })
        return False

    store_info = response.json()
    return user_id == store_info.owner
