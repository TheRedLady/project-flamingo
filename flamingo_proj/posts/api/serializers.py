from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from posts.models import Post, Like, Share


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostListSerializer(ModelSerializer):
    detail_url = HyperlinkedIdentityField(view_name='post-detail')

    class Meta:
        model = Post
        fields = ['detail_url', 'id', 'posted_by', 'content']
