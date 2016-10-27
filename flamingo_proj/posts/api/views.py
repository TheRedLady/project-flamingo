from home.utils import get_query, get_key

from posts.models import Post, Like, Tag, Share
from .serializers import (
    PostDetailSerializer,
    PostLikeSerializer,
    PostShareSerializer,
    PostTrendingSerializer,
    PostCreateSerializer,
    ShareSerializer,
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
        queryset = Post.objects.all().order_by('-created')
        posted_by = self.request.query_params.get('posted_by', None)
        if posted_by is not None:
            queryset = queryset.filter(posted_by=posted_by)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return PostDetailSerializer
        elif self.action == 'create' or self.action == 'update':
            return PostCreateSerializer
        elif self.action == 'like':
            return PostLikeSerializer
        elif self.action == 'share':
            return PostShareSerializer
        elif self.action == 'trending':
            return PostTrendingSerializer
        else:
            return PostDetailSerializer

    def create(self, request):
        new_post = Post.objects.create(posted_by=self.request.user,
                                       content=request.data['content'])
        serializer = PostDetailSerializer(new_post, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['get', 'post', 'delete'],
                  permission_classes=[IsAuthenticated, ])
    def like(self, request, pk=None):
        post = self.get_object()

        if request.method == 'GET':
            try:
                Like.objects.get(liked_by=request.user, post=post)
                return Response({
                    'status': 'True',
                    'message': 'User {} likes post {}'.format(request.user, post.id),
                    'liked': True,
                })
            except Like.DoesNotExist:
                return Response({
                    'status': 'False',
                    'message': "User {} doesn't currently like post {}".format(request.user, post.id),
                    'liked': False,
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
                    'message': 'User {} likes post {}'.format(request.user, post.id),
                    'liked': True,
                    })
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            deleted = Like.objects.filter(liked_by=request.user, post=post).delete()
            print "DELETED ", deleted
            return Response({
                'status': 'True',
                'message': "User {} unliked like post {}".format(request.user, post.id),
                'liked': False,
                })
        else:
            return Response({'status': 'False',
                             'error': 'Something went wrong with the like'})

    @detail_route(methods=['get', 'post'],
                  permission_classes=[IsAuthenticated, ])
    def share(self, request, pk=None):
        original_post = self.get_object()
        if request.method == 'GET':
            serializer = PostDetailSerializer(original_post, context={'request': request})
            shares = Share.objects.filter(original_post=original_post)
            serializer = ShareSerializer(shares, many=True, context={'request': request})
            return Response(serializer.data)
        if request.method == 'POST':
            shared_post = Post.objects.create(posted_by=request.user,
                                              content=original_post.content)
            share = Share.objects.create(original_post=original_post, shared_post=shared_post)
            data = {
                'original_post': PostShareSerializer(original_post, context={'request': request}).data,
                'shared_post': PostShareSerializer(shared_post, context={'request': request}).data,
            }
            serializer = ShareSerializer(data=data)
            if serializer.is_valid():
                serializer = PostDetailSerializer(shared_post, context={'request': request})
                return Response(serializer.data)
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

    @list_route(permission_classes=[IsAuthenticated, ])
    def feed(self, request):
        logged_user = request.user
        posts = Post.objects.filter(posted_by__in=
                                    [fol.user.id for fol in logged_user.profile.follows.all()]).order_by('-created')
        posts = Post.add_liked_by_user(posts, request.user)
        Post.add_shared_property(posts)
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(posts, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class PostsSearchAPIView(ListAPIView):
    serializer_class = PostDetailSerializer

    def get_queryset(self):
        q = self.kwargs['q']
        posts_query = get_query(q, ['tag__tag'], tag=True)
        posts = Post.objects.filter(posts_query).order_by('-created').distinct()
        return posts
