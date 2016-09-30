from posts.models import Post, Tag, Like, Share
from django.shortcuts import render

from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from posts.models import Post
from .serializers import (
    PostDetailSerializer,
    PostListSerializer,)


class PostAPIViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        serializer = PostListSerializer(queryset, many=True,
                                        context={'request': request})
        return Response(serializer.data)
