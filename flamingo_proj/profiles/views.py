from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse
from models import Profile
from posts.models import Post


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        posts = Post.objects.filter(
            posted_by=self.object.user.id).order_by('-created')
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['posts'] = Post.add_liked_by_user(posts, self.request.user)
        Post.add_shared_property(context['posts'])
        return context


class GoToProfile(LoginRequiredMixin, generic.base.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        kwargs['pk'] = self.request.user.id
        self.url = '/profile/{}/'.format(kwargs['pk'])
        return super(GoToProfile, self).get_redirect_url(*args, **kwargs)
