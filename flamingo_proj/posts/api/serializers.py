from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from posts.models import Post, Like, Share


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']


class PostDetailSerializer(ModelSerializer):
    delete_url = HyperlinkedIdentityField(
        view_name='posts-api:delete'
    )
    edit_url = HyperlinkedIdentityField(
        view_name='posts-api:edit'
    )

    class Meta:
        model = Post
        fields = '__all__'


class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='posts-api:detail'
    )

    class Meta:
        model = Post
        fields = ['url', 'id', 'content', 'posted_by']


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['liked_by', 'post']
        read_only_fields = ['liked_by', 'post']


class PostShareSerializer(ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'