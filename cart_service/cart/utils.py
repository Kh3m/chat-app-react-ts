import logging
import json

import redis

from django.core.serializers.json import DjangoJSONEncoder


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

logger = logging.getLogger(__name__)


def get_guest_cart_id():
    return redis_client.get('guest_cart_id')


def set_guest_cart_id(cart_id: str):
    redis_client.set('guest_cart_id', str(cart_id))


def get_or_create_auth_cart(user_id: int):
    redis_key = f'cart:user:{user_id}'
    auth_cart_data = redis_client.get(redis_key)

    if auth_cart_data:
        return json.loads(auth_cart_data.decode('utf-8'))

    # If the cart doesn't exist in Redis, create a new cart
    auth_cart = {
        'user_id': user_id,
        'cart_items': []
    }

    # Updated Redis key for the authenticated user's cart
    redis_key = f'cart:user:{user_id}'
    redis_client.set(redis_key, json.dumps(auth_cart))
    return auth_cart


def get_existing_cart_item_redis(cart, prod_id, options_data, user_id=None):
    # Construct the Redis key based on the user_id
    redis_key = f'cart:user:{user_id}' if user_id is not None else f'cart:main:{cart["id"]}'

    print('OPTIONS DATA PARAMS: ', options_data)
    # Retrieve cart data from Redis
    cart_data_json = redis_client.get(redis_key)

    if cart_data_json:
        # If data is found, parse it from JSON
        cart_data = json.loads(cart_data_json.decode('utf-8'))
        logger.info(f'Cart detail: {cart_data} retrieved successfully')
        print(f'Cart Data to CHECK: {cart_data}')
        cart_items = cart_data.get('cart_items', [])

        logger.info(f'cart_items {cart_items} retrieved successfully')
        # print(f'cart_items {cart_items} retrieved successfully')

        for cart_item_data in cart_items:
            logger.info(f'Cart Item: {cart_item_data}')
            # print(f'Loop checking Cart Item: {cart_item_data}')
            if cart_item_data['prod_id'] == prod_id:
                # Check if the cart item matches the product ID
                options = cart_item_data.get('item_options', [])
                print('ALL OPTIONS: ', options)

                # Check if options_data is contained in any of the cart item options
                for option in options:
                    if (all(key in option and option[key] == value for key, value in options_data_item.items()) for
                           options_data_item in options_data):
                        print('IT IS CONTAINED')
                        print(f'Merging new CartItem with CartItem with ID {cart_item_data['id']}')
                        logger.info(f'Cart with ID {cart_item_data["id"]} matches the current cart item')
                        return cart_item_data

            # If no matching item is found, return None
        return None


def merge_cart_items(cart, cart_item, quantity_to_add):
    # Update the quantity of the existing cart item
    cart_item['quantity'] += quantity_to_add
    logger.info(f'New CartItem quantity = {cart_item["quantity"]} + {quantity_to_add}')

    # Find the index of the cart_item in the cart_items list
    for index, item in enumerate(cart['cart_items']):
        if item['id'] == cart_item['id']:
            # Replace the existing item with the updated item
            cart['cart_items'][index] = cart_item
            break

    # Save the updated cart data back to Redis
    redis_user_key = f'cart:user:{cart["user_id"]}' if cart["user_id"] else None
    redis_cart_key = f'cart:main:{cart["id"]}'
    redis_cart_item_key = f'cart_item:main:{cart_item['id']}'
    redis_cart_other_key = f'cart_item:cart:{cart["id"]}:{cart_item['id']}'

    if redis_user_key:
        redis_client.set(redis_user_key, json.dumps(cart, cls=DjangoJSONEncoder))
    redis_client.set(redis_cart_key, json.dumps(cart, cls=DjangoJSONEncoder))
    redis_client.set(redis_cart_other_key, json.dumps(cart_item, cls=DjangoJSONEncoder))
    redis_client.set(redis_cart_item_key, json.dumps(cart_item, cls=DjangoJSONEncoder))
    logger.info(f'Cart with ID {cart["id"]} saved to Redis successfully')


def get_cart_from_redis(cart_id=None, user_id=None):
    cart_data_json = redis_client.get(f'cart:main:{cart_id}')
    user_cart_data_json = redis_client.get(f'cart:user:{user_id}')
    print(cart_data_json, user_cart_data_json)

    if cart_data_json:
        logger.info(f"Cart with ID {cart_id} retrieved from Redis successfully")
        return json.loads(cart_data_json.decode('utf-8'))
    elif user_cart_data_json:
        logger.info(f"Cart with User ID {user_id} retrieved from Redis successfully")
        return json.loads(user_cart_data_json.decode('utf-8'))
    return None


def delete_cart_from_redis(cart_id, user_id=None):
    if user_id:
        redis_user_key = f'cart:user:{user_id}'
        redis_client.delete(redis_user_key)
    redis_cart_key = f'cart:main:{cart_id}'
    redis_client.delete(redis_cart_key)
    logger.info(f'Cart with ID {cart_id} deleted from Redis successfully')


def delete_cart_item_from_redis(cart_item_id, cart_id=None):
    if cart_id:
        redis_client.delete(f'cart_item:cart:{cart_id}:{cart_item_id}')
    redis_client.delete( f'cart_item:main:{cart_item_id}')
    logger.info(f'Cart Item with ID {cart_item_id} deleted from Redis successfully')
