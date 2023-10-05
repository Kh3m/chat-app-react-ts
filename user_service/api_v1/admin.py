from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api_v1.models import User, Address, Profile

# Register your models here.
admin.site.register(Address)
admin.site.register(Profile)
admin.site.register(User, UserAdmin)
