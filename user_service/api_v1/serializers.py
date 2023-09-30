from rest_framework import serializers
from django.contrib.auth.models import Group

from api_v1.models import User, Profile, Address


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)
    profile = serializers.HyperlinkedIdentityField(
        view_name='profile-detail', format="html", read_only=True)

    class Meta:
        model = User
        exclude = ('groups', 'username', 'user_permissions', 'is_staff')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.HyperlinkedIdentityField(
        view_name="user-detail", format="html", read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.HyperlinkedIdentityField(
        view_name="user-detail", format="html", read_only=True)

    class Meta:
        model = Address
        fields = '__all__'
