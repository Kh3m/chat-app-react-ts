from django.contrib import admin
from .models import Review, Comment


class ReviewModel(admin.ModelAdmin):
    list_display = ('user_id', 'prod_id', 'rating', 'review_text', 'is_deleted', 'created_at')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('-rating',)


class CommentModel(admin.ModelAdmin):
    list_display = ('id', 'review', 'comment_text', 'is_deleted', 'created_at')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('comment_text',)


admin.site.register(Review, ReviewModel)
admin.site.register(Comment, CommentModel)
