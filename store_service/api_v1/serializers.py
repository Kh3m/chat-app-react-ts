from rest_framework import serializers
from .models import Store, Member, Social


class StoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Store
        fields = '__all__'


class MemberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Member
        fields = '__all__'


class SocialSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Social
        fields = '__all__'
