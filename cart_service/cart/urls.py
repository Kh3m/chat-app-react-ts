from django.urls import path

from . import views

# ●	POST /carts: Creates a new cart for a user (guest or authenticated).
# ●	GET /carts/all: List all available carts for admin management
# ●	GET /carts/{cart_id}: Retrieves cart details by cart ID.
# ●	GET /carts/user/{user_id}: Retrieves a user's cart.
# ●	POST /carts/{cart_id}/items: Adds items to the cart.
# ●	GET /carts/{cart_id}/items/{item_id}: Retrieve an item from the cart.
# ●	PUT /carts/{cart_id}/items/{item_id}: Updates the quantity of an item in the cart.
# ●	DELETE /carts/{cart_id}/items/{item_id}: Removes an item from the cart.
# ●	POST /carts/{cart_id}/checkout: Initiates the checkout process from the cart.
# ●	DELETE /carts/{cart_id}/: Remove a cart entirely.

urlpatterns = [
    path('carts/', views.CreateUserCartView.as_view(), name='cart.create'),
    path('carts/all/', views.ListCartView.as_view(), name='cart.all'),
    path('options/all/', views.ListOptionsView.as_view(), name='options.all'),
    path('carts/<uuid:pk>/items/', views.AddCartItemView.as_view(), name='cart.item.add'),
    path('carts/<uuid:pk>/', views.RetrieveDeleteCartView.as_view(), name='cart.retrieve.destroy'),
    path('carts/user/<int:user_id>/', views.RetrieveUserCartView.as_view(), name='cart.user.retrieve'),
    path('carts/<uuid:cart_id>/items/<int:pk>/', views.RetrieveUpdateDestroyCartItemView.as_view(),
         name='cart.item.modify'),

    path('carts/<int:user_id>/merge', views.MergeGuestAndAuthCartsView.as_view(), name='cart.merge'),
    path('carts/<uuid:pk>/checkout/', views.CartCheckoutView.as_view(), name='cart.checkout'),
]
