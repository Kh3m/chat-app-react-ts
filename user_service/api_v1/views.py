from api_v1.models import User, Profile, Address
from api_v1.serializers import UserSerializer, ProfileSerializer
from api_v1.serializers import GroupSerializer, AddressSerializer

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


class UserViewSet(viewsets.ModelViewSet):
    """Manage Users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # Automatically creates a profile for a user
        Profile.objects.create(user=user, picture="image_url")

    @extend_schema(request=GroupSerializer, responses=GroupSerializer)
    @action(detail=True, methods=['get'], url_path='groups')
    def groups(self, request, pk=None):
        """Get groups a user belongs to."""
        user = self.get_object()
        groups = user.groups.all()
        serializer = GroupSerializer(groups, many=True)
        return Response({'user_id': user.id, 'groups': serializer.data})

    # Commented out. I don't think this is necessary:
    """"
    @extend_schema(request=ProfileSerializer, responses=ProfileSerializer)
    @action(detail=True, methods=['get', 'put', 'patch', 'delete'], url_path='profile')
    def profile(self, request, pk=None):
        user = self.get_object()
        profile = Profile.objects.get(user=user)

        if request.method == 'GET':
            serializer = ProfileSerializer(
                profile, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method in ['POST', 'PUT', 'PATCH']:

            serializer = ProfileSerializer(
                profile, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    """


class ProfileViewSet(viewsets.ModelViewSet):
    """Manage Profiles"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class AddressViewSet(viewsets.ModelViewSet):
    """Manage Profiles"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
