from posts.models import Post, Tag, Like, Share
from django.shortcuts import render

from posts.models import Post, Like
from .serializers import (
    PostDetailSerializer,
    PostListSerializer,
    PostLikeSerializer,
    )
from .permissions import PostsPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class PostAPIViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (PostsPermissions,)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'like':
            return PostLikeSerializer
        else:
            return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    @detail_route(methods=['get', 'post', 'delete'],
                  permission_classes=[IsAuthenticated, ])
    def like(self, request, pk=None):
        post = self.get_object()
        serializer = PostLikeSerializer(data=request.data)

        if request.method == 'GET':
            try:
                Like.objects.get(liked_by=request.user, post=post)
                return Response({
                    'status': 'True',
                    'message': 'User {} likes post {}'.format(request.user, post.id)
                })
            except Like.DoesNotExist:
                return Response({
                    'status': 'False',
                    'message': "User {} doesn't currently like post {}".format(request.user, post.id)
                })

        elif request.method == 'POST':
            data = {
                'post': post,
                'liked_by': request.user,
            }
            serializer = PostLikeSerializer(data=data)

            if serializer.is_valid():
                print serializer.data
                serializer.save()
                return Response({
                    'status': 'True',
                    'message': 'User {} likes post {}'.format(request.user, post.id)
                    })
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            deleted = Like.objects.filter(liked_by=request.user, post=post).delete()
            print "DELETED ", deleted
            return Response({
                'status': 'True',
                'message': "User {} unliked like post {}".format(request.user, post.id)
                })
        else:
            return Response({'status': 'False',
                             'error': 'Something went wrong with the like'})

    @detail_route(methods=['post'],
                  permission_classes=[IsAuthenticated, ])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PostLikeSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
