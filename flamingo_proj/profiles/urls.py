from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^$', views.GoToProfile.as_view(), name='go-to-profile'),
    url(r'^(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^(?P<id>[0-9]+)/follow/$', views.follow_user, name='follow'),
]
