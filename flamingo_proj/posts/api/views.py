from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    )
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
    )

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsOwnerOrReadOnly
from posts.models import Post, Tag, Like, Share
from .serializers import (
    PostDetailSerializer,
    PostListSerializer,
    PostCreateUpdateSerializer,
    PostLikeSerializer
    )


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostByTagAPIView(ListAPIView):
    model = Post
    serializer_class = PostListSerializer

    def get_queryset(self, *args, **kwargs):
        requested_tag = Tag.objects.get(tag='#' + self.kwargs['tag'])
        posts = Post.objects.filter(tag=requested_tag).order_by('-created')
        return posts


# Tova view moje da vryshta samo 1 element zashtoto izpylnqva get()
# Inache vryshta greshka
class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    # lookup_field = 'posted_by'  -  po koe pole ot modela tyrsim
    # lookup_url_kwarg = 'field2'  -  kak da se kazva to v url patterna


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class PostEditAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = PostLikeSerializer
    lookup_field = 'id'

    @detail_route(methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def like(self, request, id=None):
        user = self.request.user.id
        try:
            post = Post.objects.get(id)
        except:
            Response({"status": "Error: No post with id {}".format(id)})

        if request.method == 'GET':
            try:
                Like.objects.get(liked_by=user, post=post)
                return Response({"status": "Post {} IS liked by {}".format(id, user)})
            except:
                return Response({"status": "Post {} is NOT liked by {}".format(id ,user)})

        if request.method == 'POST':
            Like.objects.get_or_create(liked_by=user, post=post)
            return Response({"status": "You liked this post {}".format(post.content)})

    # @detail_route(methods=['get', 'post'], permission_classes=[IsAuthenticated])
    # def unlike(self, request, pk=None):
    #     profile = self.get_object()
    #     current_profile = Profile.objects.get(user_id=self.request.user.id)
    #     profile_data = ProfileDetailSerializer(profile).data
    #     profile_data['status'] = ''
    #     if profile.user_id == current_profile.user_id:
    #         profile_data['status'] = 'User cannot follow self.'
    #         return Response(profile_data)
    #     if request.method == 'GET':
    #         if current_profile in profile.followed_by.all():
    #             profile_data['status'] = 'You are following this user.'
    #         else:
    #             profile_data['status'] = 'You are not following this user.'
    #         return Response(profile_data)
    #     if request.method == 'POST':
    #         if current_profile not in profile.followed_by.all():
    #             profile_data['status'] = 'You are not following this user.'
    #         else:
    #             current_profile.follows.remove(profile)
    #             current_profile.save()
    #             profile_data['status'] = 'You are no longer following this user.'
    #         return Response(profile_data)
