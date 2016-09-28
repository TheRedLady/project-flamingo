from django.conf.urls import url


from .views import (
    ProfileCreateAPIView,
    ProfileDetailAPIView,
    ProfileEditAPIView,
    ProfileDeleteAPIView,
    ProfileListAPIView,
    ProfileViewSet,
)


user_follow = ProfileViewSet.as_view({'get': 'follow', 'post': 'follow'})
user_unfollow = ProfileViewSet.as_view({'get':'unfollow', 'post': 'unfollow'})


urlpatterns = [
    url(r'^$', ProfileListAPIView.as_view(), name='list'),
    url(r'^create/$', ProfileCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/$', ProfileDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', ProfileEditAPIView.as_view(), name='edit'),
    url(r'^(?P<pk>[0-9]+)/delete/$', ProfileDeleteAPIView.as_view(), name='delete'),
    url(r'^(?P<pk>[0-9]+)/follow/$', user_follow, name='follow'),
    url(r'^(?P<pk>[0-9]+)/unfollow/$', user_unfollow, name='unfollow'),
]
