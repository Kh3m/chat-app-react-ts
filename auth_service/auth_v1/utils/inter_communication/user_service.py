import logging
import requests

logger = logging.getLogger("auth_v1")


def get_user_cert(auth_token):
    """
    Get's a user's certificate.
    Returns user's certificate if no error. Otherwise, None
    """
    url = "http://127.0.0.1:8000/api/v1/auth/cert/"
    data = {'token': auth_token}
    response = requests.post(url=url, data=data)

    if response.status_code != 200:
        logger.error({
            'message': f"Failed to get user cert for auth token: {auth_token}",
            'detail': f"Error {response.status_code} - {response.json()['error']}"
        })
        return None

    return response.json()


def check_user_ownership(resource_id, user_id):
    """
    Returns True if the user with the user_id is the
    owner of the resource with ID resouce_id.
    """
    url = f"http://localhost:8000/api/v1/users/{resource_id}/"
    response = requests.get(url=url)

    if response.status_code != 200:
        logger.error({
            'message': f"Failed to verify ownership with Users Service",
            'detail': f"Error {response.status_code} - {response.json()['error']}"
        })
        return False

    user_info = response.json()
    return user_id == user_info['id']
