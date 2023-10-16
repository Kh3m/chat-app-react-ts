import requests


def get_user_cert(auth_token):
    """
    Get's a user's certificate.
    Returns user's certificate if no error. Otherwise, None
    """
    url = "http://127.0.0.1:8000/api/v1/auth/cert/"
    data = {'token': auth_token}
    response = requests.get(url=url, data=data)

    if response.status_code == 200:
        return response.json()
    
    return None