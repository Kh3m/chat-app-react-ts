from django.urls import reverse
from rest_framework import serializers
from django.contrib.auth.models import Group

from api_v1.models import User, Profile, Address


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('groups', 'username', 'user_permissions', 'is_staff')

    def get_profile(self, instance):
        request = self.context['request']
        if instance.profile:
            return request.build_absolute_uri(reverse('profile-detail', kwargs={'pk': instance.profile.id}))
        return None


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_user(self, instance):
        request = self.context['request']
        if instance.user:
            return request.build_absolute_uri(reverse('user-detail', kwargs={'pk': instance.user.id}))
        return None


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Address
        fields = '__all__'
