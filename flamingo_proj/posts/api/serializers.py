from rest_framework.serializers import (ModelSerializer,
                                        HyperlinkedIdentityField,
                                        SerializerMethodField,
                                        DateTimeField)

from posts.models import Post, Like, Share, Tag
from profiles.api.serializers import PostedBySerializer


class PostDetailSerializer(ModelSerializer):
    posted_by = PostedBySerializer(read_only=True)
    url = HyperlinkedIdentityField(view_name='posts:detail')
    share = SerializerMethodField()
    like_count = SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['content']

    def get_share(self, obj):
        try:
            share = Share.objects.get(shared_post_id=obj.id)
            data = {'original_post_id': share.original_post.id,
                    'original_post': share.original_post.get_absolute_url()}
            return data
        except Share.DoesNotExist:
            return None

    def get_like_count(self, obj):
        return obj.likes.count()


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']
        read_only_fields = ['posted_by']


class PostListSerializer(ModelSerializer):
    detail_url = HyperlinkedIdentityField(view_name='post-detail')
    posted_by_name = SerializerMethodField()

    def get_posted_by_name(self, obj):
        return obj.posted_by.get_full_name()

    class Meta:
        model = Post
        fields = ['posted_by_name', 'detail_url', 'id', 'posted_by', 'content', 'created']


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
    tag_occurrences_count = SerializerMethodField()
    tag_clean = SerializerMethodField()

    def get_tag_occurrences_count(self, obj):
        return obj.occurrences_count

    def get_tag_clean(self, obj):
        return obj.tag[1:]

    class Meta:
        model = Tag
        fields = ['tag_clean', 'tag_occurrences_count']
