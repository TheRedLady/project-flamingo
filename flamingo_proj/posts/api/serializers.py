from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, DateTimeField
from django.urls import reverse

from posts.models import Post, Like, Share, Tag
from profiles.api.serializers import PostedBySerializer


class PostDetailSerializer(ModelSerializer):
    posted_by = PostedBySerializer(read_only=True)
    url = HyperlinkedIdentityField(view_name='posts:detail')
    created = DateTimeField(format="%b %-d, %Y, %H:%M", read_only=True)
    modified = DateTimeField(format="%b %-d, %Y, %H:%M", read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['content']


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']


class PostListSerializer(ModelSerializer):
    detail_url = HyperlinkedIdentityField(view_name='post-detail')

    class Meta:
        model = Post
        fields = ['detail_url', 'id', 'posted_by', 'content']


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'liked_by']
        read_only_fields = ['post', 'liked_by']


class PostShareSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='post-detail')
    class Meta:
        model = Post
        fields = ['id', 'url']


class ShareSerializer(ModelSerializer):
    original_post = PostShareSerializer()
    shared_post = PostShareSerializer()
    class Meta:
        model = Share
        fields = ['original_post', 'shared_post']
        read_only_fields = ['original_post', 'shared_post']


class PostTrendingSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag']
