from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, DateTimeField
from posts.models import Post, Like, Share, Tag


class PostDetailSerializer(ModelSerializer):
    posted_by_url = SerializerMethodField()
    posted_by_name = SerializerMethodField()
    post_url = HyperlinkedIdentityField(view_name='posts:detail')
    # created = DateTimeField(format="%b %-d, %Y, %H:%M")

    def get_posted_by_url(self, obj):
        return obj.posted_by.get_absolute_url()

    def get_posted_by_name(self, obj):
        return obj.posted_by.get_full_name()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['posted_by', 'id', 'posted_by_url', 'post_url']


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['posted_by']

    def create(self, validated_data):
        post = Post(posted_by=validated_data['posted_by'], content=validated_data['content'])
        post.save()
        post.create_hashtags()
        post.save()
        return post


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
    class Meta:
        model = Share
        fields = ['original_post', 'shared_post']
        read_only_fields = ['original_post', 'shared_post']


class PostTrendingSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag']
