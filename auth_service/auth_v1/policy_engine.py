import logging
from datetime import datetime
from django.core.cache import cache

from auth_v1.utils.rate_limiter import RateLimiter

from .utils.helpers import response
from .utils.inter_communication import communicate
from .utils.helpers import get_ids_from_path, load_service_policy
from .utils.helpers import check_required_groups, check_required_permissions

logger = logging.getLogger("auth_v1")
POLICY_DIR = "/home/chigozirim/Documents/Leptons/fixam/auth_service/auth_v1/policies"

# Associate microservice names with their respective policy file paths
policies = {
    'users': f'{POLICY_DIR}/user_service',
    'products': f'{POLICY_DIR}/product_service',
}


def evaluate_policy(auth_token=None, req_path=None, method=None, service=None):
    """
    Evaluate the access policy for a requested resouce and user.

    This function checks the provided path and method against the access
    policies defined for the service. It determines if the user has the 
    necessary permissions and belongs to the required groups to access the
    specified resource.

    Args:
        auth_token (str): User's authorization token
        req_path (str): Path to the resouce being accessed
        method (str): HTTP method being used (e.g., "GET", "POST", "PUT", "DELETE")
        service (str): Micro service the requested resouce belongs to (e.g., "users")

    Returns:
        dict: A dictionary containing authorization status, HTTP status code, and a message.
            - bool: True if the user is authorized to access the endpoint, False otherwise.
            - int: HTTP status code representing the outcome of the authorization check.
                200: Authorized access.
                404: Requested service doesn't exist
                401: Authentication failure.
                429: Too many request (user has exceeded rate limit)
                403: Forbidden (unauthorized) access.
                500: Failed to load policy for the service (internal server error).
            - message: Message for the response
    """
    service_policy_path = policies.get(service)
    if service_policy_path is None:
        logger.error({
            "message": f'requested service [{service}] not found',
            'detail': f"policies (dict) does not have the key '{service}'"
        })
        return response(False, 404, f'requested service [{service}] not found')

    service_policy_file = f"{service_policy_path}.json"
    service_policy = load_service_policy(service_policy_file)
    if service_policy is None:
        logger.error({
            "message": f"Failed to load policy for {service}",
            'detail': f"Policy file not found: {service_policy_file}"
        })
        return response(False, 500, f"Failed to load policy for {service}")

    resource_endpoint, resource_policy = get_resource_policy(
        service_policy, req_path, method)

    if not resource_policy:
        detail = {'req_path': req_path, 'method': method}
        logger.info(f"No policy found for resource: {detail}")
        return response(False, 403, 'No policy found for resource')

    must_authenticate = resource_policy.get('authenticate', True)
    required_groups = resource_policy.get('groups', [])
    required_permissions = resource_policy.get('permissions', [])

    user_cert = authenticate(auth_token)
    if not user_cert and must_authenticate:
        logger.info(f"Failed to authenticate. Auth token: {auth_token}")
        return response(False, 401, 'Authentication failed')

    # Check user rate limit
    rate_limiter = RateLimiter(service_policy['rate_limit'])
    if not rate_limiter.allow(user_cert['user_id'], user_cert['groups']):
        logger.info(f"User ({user_cert['user_id']}) rate limit reached")
        return response(False, 429, "Too many requests")

    # Check required groups
    if required_groups and not check_required_groups(user_cert, required_groups):
        logger.info(
            f"User ({user_cert['user_id']}) doesn't belong to any of the required groups")
        return response(False, 403, 'Unauthorized')

    # Check required permissions
    ids = get_ids_from_path(req_path, resource_endpoint)
    resource_id = None if not ids else ids[0]
    if required_permissions and not \
            check_required_permissions(service, user_cert, required_permissions, resource_id):
        logger.info(
            f"User ({user_cert['user_id']}) doesn't have the required permissions")
        return response(False, 403, 'Unauthorized')

    return response(True, 200, 'Success')


def authenticate(auth_token):
    """
    Validates an authorization token with the user service and caches it.

    Returns user's certificate if token is valid. Otherwise, returns None.
    """

    # Generate cache key
    if len(auth_token) < 9:
        return None
    cache_key = auth_token.split('.')[-1] \
        if '.' in auth_token else auth_token[8]
    user_cert = cache.get(cache_key)

    if user_cert is None:
        get_cert = communicate['users']['get_user_cert']
        user_cert = get_cert(auth_token)

        if user_cert and user_cert['is_active']:
            expiration = datetime.fromtimestamp(user_cert['exp'])
            cache_duration = expiration - datetime.utcnow()
            timeout = cache_duration.total_seconds()

            cache.set(cache_key, user_cert, timeout=timeout)
        else:
            return None

    return user_cert


def matches_endpoint(endpoint, req_path):
    """
    Match the request path againt a policy endpoint
    Returns True if there's a match. Otherwise, returns False
    """
    endpoint_parts = endpoint.split('/')
    req_path_parts = req_path.split('/')

    endpoint_parts = endpoint_parts[:-1] if \
        endpoint_parts[-1] == '' else endpoint_parts
    req_path_parts = req_path_parts[:-1] if \
        endpoint_parts[-1] == '' else req_path_parts

    if len(endpoint_parts) != len(req_path_parts) \
            and endpoint_parts[-1] != '*':
        print(endpoint_parts[-1])
        return False

    for e_part, r_part in zip(endpoint_parts, req_path_parts):
        if e_part == '*':
            break
        if e_part != "{id}" and e_part != r_part:
            return False

    return True


def get_resource_policy(service_policy, req_path, method):
    """
    Retrieves the policy for the given request path and HTTP method from the
    provided service policy.

    Returns:
        tuple: A tuple containing the matched endpoint and its associated policy.
            - str: The endpoint that matches the request path.
            - dict: The policy for the matched endpoint and HTTP method.
    """
    # Strip query parameters off req_path
    req_path = req_path.split('?')[0]
    resource_policy = service_policy['endpoints'].get(
        req_path, {}).get(method, {})

    if not resource_policy:
        # If request path (req_path) has no direct match with an endpoint,
        # try matching it with endpoints that have patterns
        endpoints = service_policy['endpoints']
        for endpoint, policy in endpoints.items():
            if matches_endpoint(endpoint, req_path):
                if method not in policy.keys():
                    # Check if the method is part of combined methods, e.g., "PUT-PATCH".
                    # In this case, the method can be PATCH.
                    all_combined_methods = [
                        key for key in policy if '-' in key and method in key.split('-')]
                    for combined_methods in all_combined_methods:
                        if method in combined_methods:
                            method = combined_methods
                            break
                resource_policy = policy.get(method, {})
                if resource_policy:
                    return (endpoint, resource_policy)

    return (req_path, resource_policy)
