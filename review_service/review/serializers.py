import logging

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Review, Comment, ReportComment

logger = logging.getLogger(__name__)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user_id', 'prod_id', 'rating', 'review_text', 'is_deleted', 'created_at', 'modified_at']


class CustomReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'prod_id', 'rating', 'review_text', 'is_deleted', 'created_at', 'modified_at']

    def create(self, validated_data):
        user_id = self.context['user_id']
        logger.info(f'user_id {user_id} retrieved from url successfully')
        review = Review.objects.create(user_id=user_id, **validated_data)
        # log the creation of a new comment
        logger.info("User with ID {user_id}'s review created successfully")
        return review


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment_text', 'created_at', 'modified_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'review_id', 'comment_text', 'is_deleted', 'created_at', 'modified_at']


class CustomCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'comment_text', 'is_deleted']

        extra_kwargs = {'is_deleted': {'read_only': True, 'required': False}}

    def create(self, validated_data):
        review_id = self.context['review_id']
        logger.info(f'review_id {review_id} retrieved from url successfully')
        existing_review = get_object_or_404(Review, id=review_id)
        logger.info(f'Review with review text {existing_review.review_text} retrieved successfully')
        comment = Comment.objects.create(review_id=existing_review.id, **validated_data)
        # log the creation of a new comment
        logger.info(f"Comment with ID {comment.id} created successfully")
        return comment


class ReportReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportComment
        fields = ['id', 'comment_id', 'observation']
