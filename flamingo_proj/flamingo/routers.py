from rest_framework.routers import DefaultRouter

from posts.api.views import PostAPIViewSet

router = DefaultRouter()
router.register(r'posts', PostAPIViewSet)
