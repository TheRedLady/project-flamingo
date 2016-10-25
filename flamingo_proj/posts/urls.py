from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tag/(?P<tag>[a-zA-Z0-9]+)/$', views.posts_by_tag, name='tag'),
    url(r'^(?P<pk>[0-9]+)/$', views.PostView.as_view(), name='detail'),
    url(r'^trending/$', views.trending, name='trending'),
]
