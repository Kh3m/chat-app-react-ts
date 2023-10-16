""""""
from math import perm
import os
import json
from django.core.cache import cache

from .utils.helpers import check_required_groups, check_required_permissions, get_ids_from_path, load_service_policy
from .utils.inter_communication import get_user_cert
from .utils.inter_communication import communicate

POLICY_DIR = "./policies"

policies = {
    'users': f'{POLICY_DIR}/user_service',
    'products': f'{POLICY_DIR}/product_service',
}


def evaluate_policy(auth_token, req_path, method, service):
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

    Raises an exception if one of the arguments is missing.

    Returns:
        bool: True if the user is authorized to access the endpoint, False otherwise.
    """
    service_policy_file = f"{policies[service]}.json"
    service_policy = load_service_policy(service_policy_file)
    if service_policy is None:
        # Log or raise an error
        return False

    resource_endpoint, resource_policy = get_resource_policy(
        service_policy, req_path, method)

    if not resource_policy:
        return False

    must_authenticate = resource_policy.get('authenticate', True)
    required_groups = resource_policy.get('groups', [])
    required_permissions = resource_policy.get('permissions', [])

    user_cert = authenticate(auth_token)
    if not user_cert and must_authenticate:
        return False

    # Check required groups
    if required_groups and not check_required_groups(user_cert, required_groups):
        return False

    # Check required permissions
    resource_id = get_ids_from_path(req_path, resource_endpoint)[0]
    if required_permissions and not check_required_permissions(service, user_cert, required_permissions, resource_id):
        return False

    return True


def authenticate(auth_token):
    """
    Validates an authorization token with the user service and caches it.

    Returns user's certificate if token is valid. Otherwise, returns None.
    """

    # Generate cache key
    cache_key = auth_token.split(
        '.')[-1] if '.' in auth_token else auth_token[8]
    user_cert = cache.get(cache_key)

    if user_cert is None:
        get_cert = communicate['users']['get_user_cert']
        user_cert = get_cert(auth_token)

        if user_cert.is_active is False:
            return None

        if user_cert:
            cache.set(cache_key, auth_token, timeout=user_cert['exp'])
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

    if len(endpoint_parts) != len(req_path_parts):
        return False

    for e_part, r_part in zip(endpoint_parts, req_path_parts):
        if e_part != "{id}" and e_part != r_part:
            return False

    return True


def get_resource_policy(service_policy, req_path, method):
    """Gets the policy for an endpoint"""
    # Strip query parameters off req_path
    req_path = req_path.split('?')[0]
    endpoint_policy = service_policy.get(req_path, {}).get(method, {})

    if not endpoint_policy:
        # If request path (req_path) has no direct match with an endpoint,
        # try matching it with endpoints that have patterns
        for endpoint, policy in policies.items():
            if endpoint.endswith('*'):
                endpoint = endpoint[:-1]
                if matches_endpoint(endpoint, req_path):
                    endpoint_policy = policy.get(method, {})
                    if endpoint_policy:
                        return (endpoint, policy)

    return (req_path, endpoint_policy)
