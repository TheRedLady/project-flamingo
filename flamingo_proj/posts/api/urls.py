from django.conf.urls import url

from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostEditAPIView,
    PostCreateAPIView,
    PostByTagAPIView,
    LikeViewSet,
    ShareAPIView,
    LikeViewSetRemake,
    )


urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='list_posts'),
    url(r'^(?P<pk>\d+)/$', PostDetailAPIView.as_view(), name='detail'),
    url(r'^create/$', PostCreateAPIView.as_view(), name='create_post'),
    url(r'^(?P<pk>\d+)/edit/$', PostEditAPIView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', PostDeleteAPIView.as_view(), name='delete'),
    url(r'^tag/(?P<tag>[a-zA-Z0-9]+)/$', PostByTagAPIView.as_view(), name='tag'),
    # url(r'^(?P<id>[0-9]+)/like/$', LikeViewSet.as_view({'get': 'like', 'post': 'like'}), name='like'),
    # url(r'^(?P<id>[0-9]+)/unlike/$', LikeViewSet.as_view({'get': 'unlike', 'post': 'unlike'}), name='unlike'),
    url(r'^(?P<id>[0-9]+)/share/$', ShareAPIView.as_view(), name='share'),

    url(r'^(?P<id>[0-9]+)/likes/$', LikeViewSetRemake.as_view({'get': 'list'}), name='likes_for_post'),
    url(r'^(?P<id>[0-9]+)/like/$', LikeViewSetRemake.as_view({'get': 'retrieve',
                                                              'post': 'create',
                                                              'delete': 'destroy'}), name='like'),

    # url(r'^trending/$', views.trending, name='trending'),
]
