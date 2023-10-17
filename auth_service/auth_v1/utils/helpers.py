"""Defines helper functions"""
import os
import json
import logging
from .inter_communication import communicate

logger = logging.getLogger("auth_v1")


def get_ids_from_path(req_path, policy_endpoint):
    """
    Returns a list of all ID in a URL path.

    Args:
        req_path (str): Request URL path.
        policy_endpoint (str): Endpoint from a service policy
    """
    endpoint_parts = policy_endpoint.split('/')
    req_path_parts = req_path.split('/')

    ids = []
    for e_part, r_part in zip(endpoint_parts, req_path_parts):
        if e_part == "{id}":
            ids.append(r_part)

    return ids


def load_service_policy(policy_file_path):
    """Gets the policy for a service."""
    if os.path.exists(policy_file_path) is False:
        return None

    with open(policy_file_path, 'r') as file:
        policy = json.load(file)

    return policy


def check_required_groups(user_cert, required_groups):
    """Check if the user is a member of any required group."""
    return any(group in required_groups for group in user_cert.get('groups', []))


def check_required_permissions(service, user_cert, required_permissions, resource_id):
    """
    Checks if the user has any required permission.

    Args:
        service (str): Service name, e.g. users, products.
        user_cert (dict): User certificate
        required_permissions (list): A list of required permissions
        resource_id: (str): ID of the targeted resource.

    Returns:
        bool: True if the user has the necessary permissions to meet the
              requirements. Otherwise, False
    """
    for permission in required_permissions:
        if permission == 'OWNER':
            check_ownership = communicate[service]['check_ownership']
            if check_ownership(resource_id, user_cert['user_id']):
                return True

        if permission == 'STORE_MEMBER':
            check_store_membership = communicate[service]['check_membership']
            if check_store_membership(resource_id, user_cert['user_id']):
                return True

        if permission in user_cert['permissions']:
            return True

    return False
