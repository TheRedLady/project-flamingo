"""flamingo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from posts.api.views import PostsByTagAPIView, PostsSearchAPIView
from profiles.api.views import ProfilesSearchAPIView
from home.api.views import PostsByFollowedAPIView
from messaging.views import messaging

from .routers import router


urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('home.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^profile/', include('profiles.urls', namespace='profiles')),
    url(r'^messaging/', messaging),
    url(r'^posts/', include('posts.urls', namespace='posts')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api/feed/$', PostsByFollowedAPIView.as_view(), name='feed'),
    url(r'^api/posts/tag/(?P<tag>[a-zA-Z0-9]+)/$', PostsByTagAPIView.as_view(), name='posts-by-tag'),
    url(r'^api/posts/search/(?P<q>[a-zA-Z0-9]+)/$', PostsSearchAPIView.as_view(), name='search'),
    url(r'^api/profiles/search/(?P<q>[a-zA-Z0-9]+)/$', ProfilesSearchAPIView.as_view(), name='search')
]
