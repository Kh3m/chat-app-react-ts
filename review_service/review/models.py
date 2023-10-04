from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class ActiveReviewCommentManager(models.Manager):
    def get_queryset(self):
        return super(ActiveReviewCommentManager, self).get_queryset().filter(is_deleted=False)


class InactiveReviewCommentManager(models.Manager):
    def get_queryset(self):
        return super(InactiveReviewCommentManager, self).get_queryset().filter(is_deleted=True)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        abstract = True


class Review(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, null=True)
    prod_id = models.CharField(max_length=50)
    rating = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(limit_value=1, message='Rating must be at least 1'),
            MaxValueValidator(limit_value=5, message='Rating must be at most 5'),
        ]
    )
    review_text = models.TextField()
    is_deleted = models.BooleanField(default=False)

    active_reviews = ActiveReviewCommentManager()
    inactive_reviews = InactiveReviewCommentManager()

    def __str__(self):
        return str(self.review_text[:15])


class Comment(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=50)
    comment_text = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    active_comments = ActiveReviewCommentManager()
    inactive_comments = InactiveReviewCommentManager()

    def __str__(self):
        return str(self.comment_text[:15])


class ReportComment(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    observation = models.CharField(max_length=200)

    def __str__(self):
        return str(self.observation[:15])
