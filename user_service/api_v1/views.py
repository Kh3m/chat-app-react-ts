from api_v1.models import User, Profile, Address
from api_v1.serializers import UserSerializer, ProfileSerializer
from api_v1.serializers import GroupSerializer, AddressSerializer

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import Group
from drf_spectacular.utils import extend_schema


class UserViewSet(viewsets.ModelViewSet):
    """Manage Users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # Automatically creates a profile for a user, if one does not exist
        profile = Profile.objects.filter(user=user).first()
        if not profile:
            profile = Profile.objects.create(user=user, picture="image_url")
            user.profile = profile
            user.save()

    @extend_schema(request=GroupSerializer, responses=GroupSerializer)
    @action(detail=True, methods=['get', 'post', 'put'], url_path='groups')
    def groups(self, request, pk=None):
        """
        Mange user groups.

        **GET**
        : Retieve groups a user belongs to

        **POST**
        : Add a user to a group

        **PUT**
        : Remove a user from a group
        """
        user = self.get_object()

        if request.method == 'GET':
            groups = user.groups.all()
            serializer = GroupSerializer(groups, many=True)
            return Response({'user_id': user.id, 'groups': serializer.data})

        elif request.method == 'POST':
            group_name = request.data.get('name')
            if not group_name:
                return Response({'error': 'Invalid request data. Missing group name.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                group = Group.objects.get(name=group_name)
                if group not in user.groups.all():
                    user.groups.add(group)
                    user.save()
                    return Response({'message': f"User added to {group.name}'s group successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': f'User is already a member of {group.name}'})
            except Group.DoesNotExist:
                return Response({'error': f'The group {group_name} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            group_name = request.data.get('name')
            if not group_name:
                return Response({'error': 'Invalid request data. Missing group name.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                group = Group.objects.get(name=group_name)
                if group in user.groups.all():
                    user.groups.remove(group)
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({'error': f"User not a member of {group.name}' group"})

            except Group.DoesNotExist:
                return Response({'error': f'Group with name {group_name} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    # Commented out. I don't think it's necessary:
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
