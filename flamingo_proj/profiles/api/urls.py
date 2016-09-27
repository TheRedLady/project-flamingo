from django.conf.urls import url


from .views import (
    ProfileCreateAPIView,
    ProfileDetailAPIView,
    ProfileEditAPIView,
    ProfileDeleteAPIView,
)


urlpatterns = [
    url(r'^create/$', ProfileCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/$', ProfileDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', ProfileEditAPIView.as_view(), name='edit'),
    url(r'^(?P<pk>[0-9]+)/delete/$', ProfileDeleteAPIView.as_view(), name='delete'),

]
