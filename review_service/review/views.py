import logging

from rest_framework import generics, status
from rest_framework.views import APIView

from .models import Review, Comment, ReportComment
from .pagination import PageNumberPagination

# Create your views here.
from .serializers import (
    ReviewSerializer,
    CustomReviewSerializer,
    CommentSerializer,
    CustomCommentSerializer,
    CommentUpdateSerializer,
    ReportReviewSerializer
)

from rest_framework.response import Response

logger = logging.getLogger(__name__)


class ListAllReviewsView(generics.ListAPIView):
    """
    API View for listing all submitted reviews by customers.

    This view that allows an admin to view all submitted reviews in the system.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # log the retrieval of user_id from url
        logger.info(f"All reviews retrieved successfully.")
        return super(ListAllReviewsView, self).list(self, request, *args, **kwargs)


class ListAllCommentsView(generics.ListAPIView):
    """
    API View for listing all submitted comments by customers.

    This view that allows an admin to view all submitted comments in the system.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # log the retrieval of user_id from url
        logger.info(f"All comments retrieved successfully.")
        return super(ListAllCommentsView, self).list(self, request, *args, **kwargs)


class ListCreateCustomerReviewView(generics.ListCreateAPIView):
    """
    API View for creating and listing customer review.

    This view that allows a customer to create a review  on a purchased product.
    """
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomReviewSerializer
        return ReviewSerializer

    def get_queryset(self):
        return Review.active_reviews.filter(user_id=self.kwargs['user_id'])

    def get_serializer_context(self):
        return {'user_id': self.kwargs['user_id']}

    def list(self, request, *args, **kwargs):
        # log the retrieval of user_id from url
        logger.info(f"User with ID {self.kwargs['user_id']}'s reviews retrieved successfully.")
        return super(ListCreateCustomerReviewView, self).list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # log the creation of a new review
        logger.info("Review created successfully")
        return super(ListCreateCustomerReviewView, self).create(request, *args, **kwargs)


class CustomRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = None
    pagination_class = PageNumberPagination
    Model = None

    def retrieve(self, request, *args, **kwargs, ):
        # log the creation of a new review
        logger.info(f"{self.Model} with ID {self.kwargs['pk']} retrieved successfully.")
        return super(CustomRetrieveUpdateDeleteView, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # log the update of a review
        logger.info(f"{self.Model} with ID {self.kwargs['pk']} updated successfully.")
        return super(CustomRetrieveUpdateDeleteView, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        item = self.Model.objects.get(id=self.kwargs['pk'])
        item.is_deleted = True
        item.save()
        logger.info(f"{self.Model} with ID {self.kwargs['pk']} deleted successfully.")
        return super(CustomRetrieveUpdateDeleteView, self).update(request, *args, **kwargs)


class RetrieveUpdateDeleteReviewView(CustomRetrieveUpdateDeleteView):
    queryset = Review.active_reviews.all()
    Model = Review

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CustomReviewSerializer
        return ReviewSerializer


class ListProductReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(prod_id=self.kwargs['prod_id'])

    def list(self, request, *args, **kwargs):
        # log the retrieval of prod_id from url
        logger.info(f"Reviews for Product with ID {self.kwargs['prod_id']} retrieved successfully")
        return super(ListProductReviewsView, self).list(self, request, *args, **kwargs)


class ListCreateCommentOnReviewView(generics.ListCreateAPIView):
    """
    API View for adding a comment to a review.

    This view that allows a customer to add a comment to a review.
    """
    pagination_class = PageNumberPagination
    lookup_field = 'review_id'

    def get_queryset(self):
        comments = Comment.active_comments.filter(review_id=self.kwargs['review_id'])
        logger.info(f'Comments {comments} successfully retrieved!')
        return comments

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializer
        return CustomCommentSerializer

    def get_serializer_context(self):
        return {'review_id': self.kwargs['review_id']}

    def list(self, request, *args, **kwargs):
        logger.info(f"All comments on review with ID {self.kwargs['review_id']} retrieved successfully")
        return super(ListCreateCommentOnReviewView, self).list(request, *args, **kwargs)


class RetrieveUpdateDeleteCommentView(CustomRetrieveUpdateDeleteView):
    queryset = Comment.active_comments.all()
    Model = Comment

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CommentUpdateSerializer
        return CommentSerializer


class ReportCommentView(generics.ListCreateAPIView):
    queryset = ReportComment.objects.all()
    serializer_class = ReportReviewSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # log the retrieval of user_id from url
        logger.info(f"List of reported comments retrieved successfully")
        return super(ReportCommentView, self).list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # log the creation of a new review
        logger.info("ReportComment created successfully")
        return super(ReportCommentView, self).create(request, *args, **kwargs)


class ReviewAverageView(APIView):
    def get(self, request, prod_id):
        reviews = Review.objects.filter(prod_id=prod_id)
        total_ratings = reviews.count()
        if total_ratings > 0:
            average_rating = sum([review.rating for review in reviews]) / total_ratings
            return Response({
                'prod_id': self.kwargs['prod_id'],
                'total_ratings': total_ratings,
                'average_rating': average_rating,
            }, status=status.HTTP_200_OK)
        return Response({
            'error': 'Product with the given ID does not exist!'
        }, status=status.HTTP_404_NOT_FOUND)
