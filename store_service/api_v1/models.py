import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Store(models.Model):
    """Manage a store"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.UUIDField(null=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=350)
    phone = PhoneNumberField()
    slug = models.CharField(max_length=30, unique=True)
    logo_img_url = models.CharField(max_length=350, null=True)
    banner_img_url = models.CharField(max_length=350, null=True)
    website = models.CharField(null=True)
    address = models.CharField(max_length=500, null=True)
    description = models.TextField(null=True, blank=True)
    business_license_number = models.CharField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(
        "Member", related_name='store_members', null=True)
    socials = models.ManyToManyField(
        "Social", related_name='store_socials', null=True)


class Member(models.Model):
    """Manage store member"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.UUIDField(unique=True)
    added_at = models.DateTimeField(auto_now_add=True)


class Social(models.Model):
    """Manage store social media"""
    CHOICES = [
        ('Twitter', 'Twitter'),
        ('Facebook', 'Facebook'),
        ('YouTube', 'YouTube'),
        ('LinkedIn', 'LinkedIn'),
        ('Instagram', 'Instagram'),
        ('WhatsApp', 'WhatsApp')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    platform = models.CharField(max_length=60, choices=CHOICES)
    link = models.CharField(max_length=60)
