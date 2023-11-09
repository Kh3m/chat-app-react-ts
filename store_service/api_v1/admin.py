from django.contrib import admin
from .models import Store, Member, Social


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'owner', 'email')
    date_hierarchy = 'created_at'


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('store', 'user', 'added_at')
    list_filter = ('store', 'added_at')
    search_fields = ('store__name', 'user')
    date_hierarchy = 'added_at'


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = ('store', 'platform', 'link')
    list_filter = ('store', 'platform')
    search_fields = ('store__name', 'platform', 'link')


# admin.site.register(Store, StoreAdmin)
# admin.site.register(Member, MemberAdmin)
# admin.site.register(Social, SocialAdmin)
