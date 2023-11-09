from django.urls import reverse
from rest_framework import serializers
from .models import Store, Member, Social
from .custom_fields import CustomHyperLinkedModelSerializer


class StoreSerializer(CustomHyperLinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)
    members = serializers.SerializerMethodField()
    socials = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = '__all__'

    def get_members(self, obj):
        request = self.context.get('request')
        if request:
            store_id = obj.id
            members = obj.members.all()
            root_uri = request.build_absolute_uri()
            member_urls = [
                request.build_absolute_uri(
                    f'{root_uri}{store_id}/members/{member.id}/')
                for member in members
            ]
            return member_urls

    def get_socials(self, obj):
        request = self.context.get('request')
        if request:
            store_id = obj.id
            socials = obj.socials.all()
            root_uri = request.build_absolute_uri()
            socials_urls = [
                request.build_absolute_uri(
                    f'{root_uri}{store_id}/socials/{social.id}/')
                for social in socials
            ]
            return socials_urls


class MemberSerializer(CustomHyperLinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = '__all__'
        lookup_field = 'store'

    def get_url(self, obj):
        request = self.context.get('request')
        url = f"{request.build_absolute_uri()}{obj.id}/"
        return url


class SocialSerializer(CustomHyperLinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Social
        fields = '__all__'
        lookup_field = 'store'
        lookup_url_kwarg = 'store'

    def get_url(self, obj):
        request = self.context.get('request')
        url = f"{request.build_absolute_uri()}{obj.id}/"
        return url
