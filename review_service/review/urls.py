from django.urls import path

from . import views

# •	POST /reviews: Submits a new review for a product. *
# •	PUT /reviews/{review_id}: Updates an existing review. *
# •	DELETE /reviews/{review_id}: Deletes a review. *
# •	GET /products/{product_id}/reviews: Retrieves reviews for a specific product. *
# •	POST /reviews/{review_id}/comments: Adds a comment to a review. *
# •	PUT /comments/{comment_id}: Updates an existing comment. *
# •	DELETE /comments/{comment_id}: Deletes a comment. *


urlpatterns = [
    path('reviews/', views.ListAllReviewsView.as_view(), name='review.list.all'),
    path('reviews/user/<int:user_id>/', views.ListCreateCustomerReviewView.as_view(), name='review.list.create'),
    path('reviews/<int:pk>/', views.RetrieveUpdateDeleteReviewView.as_view(), name='review.retrieve.update.delete'),
    path('reviews/products/<int:prod_id>/', views.ListProductReviewsView.as_view(),
         name='review.products.list'),
    path('reviews/<int:review_id>/comments/', views.ListCreateCommentOnReviewView.as_view(), name='review.comment.add'),
    path('reviews/comments/', views.ListAllCommentsView.as_view(), name='review.comment.add'),
    path('reviews/comments/<int:pk>/', views.RetrieveUpdateDeleteCommentView.as_view(), name='comment.retrieve.modify'),

    path('reviews/comment/report/', views.ReportCommentView.as_view(), name='cart.merge'),
    path('reviews/<int:prod_id>/average/', views.ReviewAverageView.as_view(), name='review_average'),
]
