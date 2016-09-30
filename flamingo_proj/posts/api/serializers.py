from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from posts.models import Post, Like, Share


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['posted_by', 'id']


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
