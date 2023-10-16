"""Defines helper functions"""
import os
import json
from .inter_communication import communicate


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
            ids.append(r_part[1:-1])

    return ids


def load_service_policy(policy_file_path):
    """Gets the policy for a service."""
    if os.path.exists(policy_file_path):
        return None

    with open(policy_file_path, 'r') as file:
        policy = json.load(file)

    return policy


def check_required_groups(user_cert, required_groups):
    """Check if the user is a member of any required group."""
    return any(group in required_groups for group in user_cert.get('groups', []))


def check_required_permissions(service, user_cert, required_permissions, resource_id):
    """Checks if the user has any required permission."""
    for permission in required_permissions:
        if permission == 'OWNER':
            check_ownership = communicate[service]['check_ownership']
            if check_ownership(resource_id, user_cert['id']):
                return True

        if permission == 'store_member - store_id':
            pass
        if permission == 'store_owner - store_id':
            pass

        if permission in user_cert['permissions']:
            return True

    return False
