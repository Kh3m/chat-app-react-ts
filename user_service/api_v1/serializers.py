from django.urls import reverse
from rest_framework import serializers
from django.contrib.auth.models import Group
from dj_rest_auth.serializers import UserDetailsSerializer

from api_v1.models import User, Profile, Address
from api_v1.utils.custom_fields import CustomHyperLinkedModelSerializer


class GroupSerializer(CustomHyperLinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class AddressSerializer(CustomHyperLinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Address
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.get('user')
        if len(user.addresses.all()) >= 3:
            raise serializers.ValidationError("Address limit exceeded.")
        
        address = Address.objects.create(**validated_data)
        user.addresses.add(address)
        return address

class UserSerializer(CustomHyperLinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)
    profile = serializers.SerializerMethodField(read_only=True)
    groups = serializers.SerializerMethodField(read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ('username', 'user_permissions', 'is_staff')

    def get_profile(self, instance):
        request = self.context['request']
        if instance.profile:
            return request.build_absolute_uri(reverse('profile-detail', kwargs={'pk': instance.profile.id}))
        return None
    
    def get_groups(self, instance):
        try:
            user_groups = []
            groups = instance.groups.all()
            [user_groups.append(group.name) for group in groups]
            return user_groups
        except Exception as e:
            # log an error.
            return []


class ProfileSerializer(CustomHyperLinkedModelSerializer):
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



class CustomUserDetailsSerializer(UserDetailsSerializer):

    class Meta:
        model = User
        exclude = (
            'username',
            'user_permissions',
            'is_staff',
            'password'
        )