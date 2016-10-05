from posts.models import Post
from profiles.models import Profile
from posts.api.serializers import PostListSerializer

from rest_framework.generics import ListAPIView


class PostsByFollowedAPIView(ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.get(user_id=user.id)
        posts = Post.objects.filter(posted_by__id__in=
                                    [prof.user_id for prof in profile.follows.all()]
                                    ).order_by('-created')
        Post.add_shared_property(posts)
        posts = Post.add_liked_by_user(posts, self.request.user)
        return posts
