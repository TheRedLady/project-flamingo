from rest_framework.routers import DefaultRouter

from posts.api.views import PostAPIViewSet
from profiles.api.views import ProfileViewSet


router = DefaultRouter()
router.register(r'posts', PostAPIViewSet, base_name='post')
router.register(r'profiles', ProfileViewSet, base_name='profile')