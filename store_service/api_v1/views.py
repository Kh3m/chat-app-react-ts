from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


from api_v1.models import Store, Member, Social
from api_v1.serializers import StoreSerializer, MemberSerializer, SocialSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    @action(
        detail=True, methods=['post'],
        url_path='members/invite', serializer_class=MemberSerializer)
    def list_add_members(self, request, pk=None):
        pass

    @action(
        detail=True, methods=['get', 'post'],
        url_path='members', serializer_class=MemberSerializer)
    def list_add_members(self, request, pk=None):
        """
        - GET: Retrieves all members
        - POST: Adds a new member
        """
        store = self.get_object()
        # Get all members
        if request.method == 'GET':
            members = store.members.all()
            serializer = MemberSerializer(
                members, many=True, context={'request': request})
            return Response(serializer.data)

        # Add new member
        data = {"store": str(store.id), **request.data}
        serializer = MemberSerializer(
            data=data, context={'request': request})

        if serializer.is_valid():
            member = serializer.save()
            store.members.add(member)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True, methods=['get', 'delete'],
        url_path='members/(?P<member_id>[0-9a-f-]+)',
        serializer_class=MemberSerializer)
    def get_del_member(self, request, pk=None, member_id=None):
        """
        - GET: Retrieves a member
        - DELETE: Deletes a member
        """
        store = self.get_object()
        try:
            member = store.members.get(id=member_id)
        except Member.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Gets a member
        if request.method == 'GET':
            member = store.members.get(id=member_id)
            serializer = MemberSerializer(member, context={'request': request})
            return Response(serializer.data)

        # Deletes a member
        store.members.remove(member)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['get', 'post'],
        url_path='socials', serializer_class=SocialSerializer)
    def list_add_socials(self, request, pk=None):
        """
        - GET: Retrieves all social accounts
        - POST: Adds a new social account
        """
        store = self.get_object()
        # Get all social accounts
        if request.method == 'GET':
            socials = store.socials.all()
            serializer = SocialSerializer(
                socials, many=True, context={'request': request})
            return Response(serializer.data)

        # Add new social account
        data = {"store": str(store.id), **request.data}
        serializer = SocialSerializer(
            data=data, context={'request': request})

        if serializer.is_valid():
            social = serializer.save()
            store.socials.add(social)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True, methods=['get', 'delete'],
        url_path='socials/(?P<social_id>[0-9a-f-]+)',
        serializer_class=SocialSerializer)
    def get_del_socaial_account(self, request, pk=None, social_id=None):
        """
        - GET: Retrieves a social account
        - DELETE: Deletes a social account
        """
        store = self.get_object()
        try:
            social = store.socials.get(id=social_id)
        except Social.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Gets a social account
        if request.method == 'GET':
            social = store.socials.get(id=social_id)
            serializer = SocialSerializer(social, context={'request': request})
            return Response(serializer.data)

        # Deletes a social accout
        store.socials.remove(social)
        social.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class SocialViewSet(viewsets.ModelViewSet):
    queryset = Social.objects.all()
    serializer_class = SocialSerializer
