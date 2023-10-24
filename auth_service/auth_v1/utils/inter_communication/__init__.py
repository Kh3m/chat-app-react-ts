"""Maps functions that communicate with other microservices."""

from auth_v1.utils.inter_communication.product_service import check_product_ownership
from .user_service import get_user_cert, check_user_ownership
from .store_service import check_membership, check_ownership

# Provide a mapping between microservices and their associated
# communication functions:
communicate = {
    # 'microservice name': {'communication functions'}
    'users': {'get_user_cert': get_user_cert, 'check_ownership': check_user_ownership},
    'stores': {'check_membership': check_membership, 'check_ownership': check_ownership},
    'products': {'check_ownership': check_product_ownership}
}
