from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from rest_framework.generics import ListAPIView


from profiles.models import Profile
from home.utils import get_query, get_key
from .permissions import UserPermission
from .utils import get_follow_status
from .serializers import (
    ProfileCreateSerializer,
    ProfileDetailSerializer,
    ProfileUpdateSerializer,
)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [UserPermission]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['user__email', 'user__first_name', 'user__last_name', 'birthdate', 'follows']

    def get_serializer_class(self):
        if self.action == 'create':
            return ProfileCreateSerializer
        if self.action == 'retrieve':
            return ProfileDetailSerializer
        if self.action == 'update':
            return ProfileUpdateSerializer
        return ProfileDetailSerializer

    @detail_route(methods=['get', 'post'])
    def follow(self, request, pk=None):
        profile = self.get_object()
        current_user = Profile.objects.get(user_id=self.request.user.id)
        profile_data = ProfileDetailSerializer(profile, context={'request': request}).data
        following = get_follow_status(current_user, profile)
        if request.method == 'GET':
            profile_data['following'] = following
            return Response(profile_data)
        if request.method == 'POST':
            if not following:
                current_user.follows.add(profile)
                current_user.save()
                following = True
            profile_data['following'] = following
            return Response(profile_data)

    @detail_route(methods=['get', 'post'])
    def unfollow(self, request, pk=None):
        profile = self.get_object()
        current_user = Profile.objects.get(user_id=self.request.user.id)
        profile_data = ProfileDetailSerializer(profile, context={'request': request}).data
        following = get_follow_status(current_user, profile)
        if request.method == 'GET':
            profile_data['following'] = following
            return Response(profile_data)
        if request.method == 'POST':
            if following:
                current_user.follows.remove(profile)
                current_user.save()
                following = False
            profile_data['following'] = following
            return Response(profile_data)


class ProfilesSearchAPIView(ListAPIView):
    serializer_class = ProfileDetailSerializer

    def get_queryset(self):
        q = self.kwargs['q']
        posts_query = get_query(q, ['user__first_name', 'user__last_name', ])
        posts = Profile.objects.filter(posts_query)
        return posts
