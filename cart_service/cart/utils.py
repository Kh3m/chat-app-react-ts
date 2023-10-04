from django.core.cache import cache
from .models import Cart, CartItem

import logging
logger = logging.getLogger(__name__)


def get_guest_cart_id():
    return cache.get(f'guest_cart')


def set_guest_cart_id(cart_id: str):
    cache.set(f'guest_cart', '358b23ad-d3aa-41b9-89b6-ead064631736', None)


def get_or_create_auth_cart(user_id: int):
    try:
        auth_cart = Cart.objects.get(user_id=user_id)
        return auth_cart
    except Cart.DoesNotExist:
        return None


def get_existing_cart_item(cart, prod_id, options_data, user_id=None,):
    if user_id is None:
        existing_cart_item = CartItem.objects.filter(
            cart_id=cart.id,
            prod_id=prod_id,
        )
    else:
        existing_cart_item = CartItem.objects.filter(
            cart_id=cart.id,
            prod_id=prod_id,
            cart__user_id=user_id
        )
    logger.info(f'Does existing_cart_item exists: {existing_cart_item.first()}')

    for option in options_data:
        logger.info(f"{option['attribute']}: {option['value']} retrieved.")
        existing_cart_item = existing_cart_item.filter(
            item_options__attribute=option['attribute'],
            item_options__value=option['value']
        )
    logger.info(f'existing_cart_item {existing_cart_item}')
    try:
        return existing_cart_item.first()
    except CartItem.DoesNotExist:
        logger.warning('No existing cart with same attributes.')
        return None


def merge_cart_items(cart_item, quantity_to_add):
    cart_item.quantity += quantity_to_add
    logger.info(f'New CartItem quantity = {cart_item.quantity} + {quantity_to_add}')
    cart_item.save()
