from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import DjangoFilterBackend, OrderingFilter


from profiles.models import Profile
from .serializers import (
    ProfileCreateSerializer,
    ProfileDetailSerializer,
    ProfileUpdateSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsNotAuthenticated


class ProfileCreateAPIView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateSerializer
    permission_classes = [IsNotAuthenticated]


class ProfileDetailEditAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ProfileDeleteAPIView(DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'update':
            return ProfileUpdateSerializer
        return ProfileDetailSerializer

    def list(self, request):
        queryset = User.objects.all()
        filter_backends = [DjangoFilterBackend, OrderingFilter]
        filter_fields = ['user__email', 'user__first_name', 'user__last_name', 'birthdate', 'follows']
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get', 'post'])
    def follow(self, request, pk=None):
        profile = self.get_object()
        current_profile = Profile.objects.get(user_id=self.request.user.id)
        profile_data = ProfileDetailSerializer(profile, context={'request': request}).data
        if profile.user_id == current_profile.user_id:
            profile_data['status'] = 'User cannot follow self.'
            return Response(profile_data)
        if request.method == 'GET':
            if current_profile in profile.followed_by.all():
                profile_data['status'] = 'You are following this user.'
            else:
                profile_data['status'] = 'You are not following this user.'
            return Response(profile_data)
        if request.method == 'POST':
            if current_profile in profile.followed_by.all():
                profile_data['status'] = 'You are already following this user.'
            else:
                current_profile.follows.add(profile)
                current_profile.save()
                profile_data['status'] = 'You are now following this user.'
            return Response(profile_data)

    @detail_route(methods=['get', 'post'])
    def unfollow(self, request, pk=None):
        profile = self.get_object()
        current_profile = Profile.objects.get(user_id=self.request.user.id)
        profile_data = ProfileDetailSerializer(profile, context={'request': request}).data
        if profile.user_id == current_profile.user_id:
            profile_data['status'] = 'User cannot follow self.'
            return Response(profile_data)
        if request.method == 'GET':
            if current_profile in profile.followed_by.all():
                profile_data['status'] = 'You are following this user.'
            else:
                profile_data['status'] = 'You are not following this user.'
            return Response(profile_data)
        if request.method == 'POST':
            if current_profile not in profile.followed_by.all():
                profile_data['status'] = 'You are not following this user.'
            else:
                current_profile.follows.remove(profile)
                current_profile.save()
                profile_data['status'] = 'You are no longer following this user.'
            return Response(profile_data)


class ProfileListAPIView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['user__email', 'user__first_name', 'user__last_name', 'birthdate', 'follows']
