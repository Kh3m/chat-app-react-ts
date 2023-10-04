import logging

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView

from .serializers import CartSerializer, RetrieveCartSerializer, CartItemSerializer, \
    CartItemQuantityUpdateSerializer
from .models import Cart, CartItem
from .utils import get_guest_cart_id, get_or_create_auth_cart, set_guest_cart_id

from rest_framework.response import Response

logger = logging.getLogger(__name__)


class MergeGuestAndAuthCartsView(APIView):
    def post(self, request, user_id):

        # Get the guest cart_id from cache
        guest_cart_id = get_guest_cart_id()
        logger.info(f'guest_cart_id {guest_cart_id} retrieved')

        # Get or create the authenticated user's cart
        auth_cart = get_or_create_auth_cart(user_id)
        logger.info(f'auth_cart {auth_cart} retrieved')

        if guest_cart_id:
            try:
                guest_cart = Cart.objects.get(id=guest_cart_id)
                logger.info(f'guest_cart {guest_cart} retrieved')
                guest_cart_items = CartItem.objects.filter(cart=guest_cart)

                if auth_cart:
                    for guest_cart_item in guest_cart_items:
                        # Check if a similar item already exists in the authenticated cart
                        existing_item = CartItem.objects.filter(
                            cart=auth_cart,
                            prod_id=guest_cart_item.prod_id,
                            item_options__in=guest_cart_item.item_options.all(),
                        ).first()

                        if existing_item:
                            existing_item.quantity += guest_cart_item.quantity
                            existing_item.save()
                        else:
                            guest_cart_item.cart = auth_cart

                            guest_cart_item.save()
                else:
                    guest_cart.user_id = user_id
                    guest_cart.save()
                    set_guest_cart_id(str(guest_cart.id))

                # Clear the guest cart and its associated cache
                guest_cart_items.delete()
                set_guest_cart_id(cart_id='')

            except Cart.DoesNotExist:
                logger.warning(f'No guest_cart_id exists')
                pass

        # Retrieve and serialize the authenticated user's cart items
        auth_cart = Cart.objects.get(user_id=user_id)
        serializer = RetrieveCartSerializer(auth_cart)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUserCartView(generics.CreateAPIView):
    """
    API View for creating user cart.

    This view creates a cart for a user which could have many cart items.
    """
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class ListCartView(generics.ListAPIView):
    """
    API View for listing all available carts for the benefit of the admin.

    This view displays all carts.
    """
    serializer_class = RetrieveCartSerializer
    queryset = Cart.objects.all()

    def list(self, request, *args, **kwargs):
        # log the creation of a new cart
        logger.info("All carts retrieved successfully")
        return super(ListCartView, self).list(request, *args, **kwargs)


class RetrieveDeleteCartView(generics.RetrieveDestroyAPIView):
    """
    API View for retrieving and deleting a cart based on its ID.

    This view allows you to retrieve and delete a cart item.
    """
    serializer_class = RetrieveCartSerializer
    queryset = Cart.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            logger.info("Method in 'GET' accessed from CartItemView")
            return RetrieveCartSerializer
        return CartSerializer

    def retrieve(self, request, *args, **kwargs):
        # log the retrieval of user_id from
        logger.info(f"cart with ID {self.kwargs['pk']} retrieved successfully")
        return super(RetrieveDeleteCartView, self).retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # log the retrieval of user_id from
        logger.info(f"cart with ID {self.kwargs['pk']} deleted successfully")
        return super(RetrieveDeleteCartView, self).delete(request, *args, **kwargs)


class RetrieveUserCartView(generics.RetrieveAPIView):
    """
    API View for retrieving cart based user ID.

    This View allows you to retrieve and update details of individual order items.
    """
    serializer_class = RetrieveCartSerializer
    queryset = Cart.objects.all()
    lookup_field = 'user_id'

    def retrieve(self, request, *args, **kwargs):
        # log the retrieval of user_id from the URL
        logger.info(f"cart for user with ID {self.kwargs['user_id']} retrieved successfully")
        return super(RetrieveUserCartView, self).retrieve(request, *args, **kwargs)


class AddCartItemView(generics.CreateAPIView):
    """
    API View for adding cart item to cart.

    This View creates adds new item to an existing cart.
    """
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['pk']}


class RetrieveUpdateDestroyCartItemView(generics.RetrieveUpdateDestroyAPIView):
    """
    API View for retrieving, updating, and deleting a cart item.

    This View creates retrieves, updates and deletes a cart item.
    """
    queryset = CartItem.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            logger.info("Method in ['PUT', 'PATCH'] accessed from CartItemView")
            return CartItemQuantityUpdateSerializer
        return CartItemSerializer

    def retrieve(self, request, *args, **kwargs):
        # log the retrieval of user_id from the URL
        logger.info(f"Cart Item with ID {self.kwargs['pk']} retrieved successfully")
        return super(RetrieveUpdateDestroyCartItemView, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # log the update of a cart item
        logger.info(f"Cart Item with ID {self.kwargs['pk']} updated successfully")
        # call the user auth endpoint to return the logged-in user_id or None
        logged_in_user_id = None

        return super(RetrieveUpdateDestroyCartItemView, self).update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # log the update of a cart item
        logger.info(f"Cart Item with ID {self.kwargs['pk']} deleted successfully")
        return super(RetrieveUpdateDestroyCartItemView, self).update(request, *args, **kwargs)


class CartCheckoutView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        # Retrieve cart items and user information from the request
        cart_items = request.data.get('cart_items', [])
        user_id = request.data.get('user_id')

        # Step 2: Check product availability and pricing (interact with Product Service)
        product_ids = [item['product_id'] for item in cart_items]

        # Step 3: Calculate the total price based on product prices and quantities

        # Step 4: Process the payment (interact with Payment Service)
        # payment_result = PaymentService.process_payment(user_id, total_price)

        # Step 5: If payment is successful, create an order (interact with Order Service)

        # If any step fails, handle the error accordingly
        return Response({'message': 'Checkout failed'}, status=status.HTTP_400_BAD_REQUEST)

#
