import logging
from unittest import result
import requests

from auth_v1.utils.inter_communication.store_service import check_membership

logger = logging.getLogger("auth_v1")


def check_product_ownership(resource_id, user_id):
    """
    Returns True if the user with the <user_id> is a member
    of the store with ID <resouce_id>.
    """
    url = f"http://localhost:8002/api/v1/products/products/{resource_id}/"
    response = requests.get(url=url)

    if response.status_code != 200:
        logger.error({
            'message': f"Failed to retrieve product [{resource_id}] info",
            'detail': f"Error {response.status_code} - {response.json()['error']}"
        })

        return False

    store_id = response['store_id']
    result = check_membership(store_id, user_id)
    print(f"result: {result}")
    return result
