from home.utils import get_query, get_key

from posts.models import Post, Like, Tag
from .serializers import (
    PostDetailSerializer,
    PostListSerializer,
    PostLikeSerializer,
    PostShareSerializer,
    PostTrendingSerializer,
    PostCreateSerializer
    )
from .permissions import PostsPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView


class PostAPIViewSet(ModelViewSet):
    permission_classes = (PostsPermissions,)

    def get_queryset(self):
        queryset = Post.objects.all()
        posted_by = self.request.query_params.get('posted_by', None)
        if posted_by is not None:
            queryset = queryset.filter(posted_by=posted_by)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return PostDetailSerializer
        elif self.action == 'create':
            return PostCreateSerializer
        elif self.action == 'like':
            return PostLikeSerializer
        elif self.action == 'share':
            return PostShareSerializer
        elif self.action == 'trending':
            return PostTrendingSerializer
        else:
            return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    @detail_route(methods=['get', 'post', 'delete'],
                  permission_classes=[IsAuthenticated, ])
    def like(self, request, pk=None):
        post = self.get_object()

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
                serializer.save(liked_by=request.user, post=post)
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
    def share(self, request, pk=None):
        original_post = self.get_object()
        shared_post = Post.objects.create(posted_by=request.user, content=original_post.content)
        if request.method == 'POST':
            data = {
                'original_post': original_post,
                'shared_post': shared_post,
            }
            serializer = PostShareSerializer(data=data)
            if serializer.is_valid():
                serializer.save(original_post=original_post, shared_post=shared_post)
                return Response({
                    'status': 'True',
                    'message': 'User {} shared post {}'.format(request.user, original_post.id)
                    })
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

    @list_route(permission_classes=[IsAuthenticated, ])
    def trending(self, request):
        trending = Tag.get_trending()

        page = self.paginate_queryset(trending)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(trending, many=True)
        return Response(serializer.data)


class PostsSearchAPIView(ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        q = self.kwargs['q']
        posts_query = get_query(q, ['tag__tag'], tag=True)
        posts = Post.objects.filter(posts_query)
        return posts
