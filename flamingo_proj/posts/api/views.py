import sys, os

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    )
from rest_framework.permissions import (
    IsAuthenticated,
    )

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin

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


class LikeViewSet(ModelViewSet, DestroyModelMixin):
    queryset = Like.objects.all()
    serializer_class = PostLikeSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    @detail_route(methods=['get', 'post'])
    def like(self, request, id=None):
        user = self.request.user
        try:
            post = Post.objects.get(id=id)
            if request.method == 'GET':
                try:
                    Like.objects.get(liked_by=user, post=post)
                    return Response({"status": "Post {} IS liked by {}".format(id, user)})
                except Like.DoesNotExist:
                    return Response({"status": "Post {} is NOT liked by {}".format(id, user)})

            elif request.method == 'POST':
                try:
                    obj, created = Like.objects.get_or_create(liked_by=user, post=post)
                    return Response({"status": "{} liked this post {}".format(user, post)})
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    return Response({"status": "Error! Exception {} occurred!".format(message)})
        except:
            return Response({"status": "Error: No post with id {}".format(id)})

    @detail_route(methods=['get', 'post'], permission_classes=[IsOwnerOrReadOnly])
    def unlike(self, request, id=None):
        user = self.request.user
        try:
            post = Post.objects.get(id=id)
            if request.method == 'GET':
                try:
                    Like.objects.get(liked_by=user, post=post)
                    return Response({"status": "Post {} IS liked by {}".format(id, user)})
                except Like.DoesNotExist:
                    return Response({"status": "Post {} is NOT liked by {}".format(id, user)})

            if request.method == 'POST':
                try:
                    like = Like.objects.get(liked_by=user, post=post)
                    like.delete()
                    return Response({"status": "{} unliked by {}".format(post, user)})
                except Like.DoesNotExist:
                    return Response({"status": "Post {} is NOT liked by {}".format(id, user)})
        except Post.DoesNotExist:
            return Response({"status": "No post with id of {}".format(id)})
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return Response({"status": "Error! Exception {} occurred!".format(message)})
