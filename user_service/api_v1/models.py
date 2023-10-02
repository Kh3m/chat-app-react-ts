import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    CHOICES = [(False, 'Customer'), (True, 'Vendor'),]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_vendor = models.BooleanField(default=False, choices=CHOICES)
    phone = PhoneNumberField(null=True)
    profile = models.OneToOneField(
        "Profile", on_delete=models.SET_NULL, null=True, related_name='user_profile')
    username = models.CharField(
        max_length=60, unique=True, null=True)
    email = models.EmailField(max_length=320, unique=True, null=False)

    def __str__(self):
        return self.first_name

    def __repr__(self):
        obj = vars(self)
        return str(obj)


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user')

    bio = models.TextField(null=True)
    picture = models.CharField(max_length=255, null=True)

    def __repr__(self):
        obj = vars(self)
        return str(obj)


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=False)
    street_address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=70)
    state = models.CharField(max_length=70)
    country = models.CharField(max_length=70, default="Nigeria")
    zip_code = models.IntegerField(null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.country}"

    def __repr__(self):
        obj = vars(self)
        return str(obj)


def create_groups(sender, **kwargs):
    Group.objects.get_or_create(name='admins')
    Group.objects.get_or_create(name='super_admins')
    Group.objects.get_or_create(name='field_workers')


models.signals.post_migrate.connect(create_groups)
