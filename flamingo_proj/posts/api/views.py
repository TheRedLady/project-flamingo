import sys, os
from .exceptions import PostNotFoundException

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView
    )
from rest_framework.permissions import (
    IsAuthenticated,
    )

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.mixins import (
    DestroyModelMixin,
    CreateModelMixin,
)

from .permissions import IsOwnerOrReadOnly
from posts.models import Post, Tag, Like, Share
from .serializers import (
    PostDetailSerializer,
    PostListSerializer,
    PostCreateUpdateSerializer,
    PostLikeSerializer,
    PostShareSerializer
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


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class PostEditAPIView(DestroyModelMixin,
                      RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class LikeViewSet(ModelViewSet, DestroyModelMixin):
    queryset = Like.objects.all()
    serializer_class = PostLikeSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

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
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return Response({"status": "Error! Exception {} occurred!".format(message)})


class LikeViewSetRemake(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = PostLikeSerializer
    lookup_field = 'id'

    # def list(self, request, *args, **kwargs):
    #     result = Like.objects.filter(post=kwargs['id'])
    #     return Response({'likes_for_post':
    #                      self.serializer_class(result, many=True).data})

    def create(self, request, *args, **kwargs):
        user = self.request.user
        try:
            post = Post.objects.get(id=kwargs['id'])
            Like.objects.get_or_create(liked_by=user, post=post)
            # return self.retrieve(request)
            return Response({"status": "True"})
        except Post.DoesNotExist:
            raise PostNotFoundException

    def retrieve(self, request, *args, **kwargs):
        try:
            Like.objects.get(post=kwargs['id'], liked_by=request.user)
            return Response({"status": "True"})
        except Like.DoesNotExist:
            # To raise an error
            return Response({"status": "False"})

    # def destroy(self, request, *args, **kwargs):
    #     try:
    #         post = Post.objects.get(id=kwargs['id'])
    #         like = Like.objects.get(liked_by=request.user, post=post)
    #         like.delete()
    #         return Response({
    #             "message": "You successfully deleted post {}".format(id),
    #             "status": "True"})
    #     except Post.DoesNotExist:
    #         raise PostNotFoundException
    def perform_destroy(self, instance):
        instance.delete()


class ShareAPIView(CreateModelMixin,
                   RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostShareSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        shares_of_post = Share.objects.filter(original_post=kwargs['id'])
        return Response({'shares_of_post': self.serializer_class(shares_of_post, many=True).data})

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
