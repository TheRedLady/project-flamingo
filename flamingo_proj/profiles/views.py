from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from models import Profile
from posts.models import Post


class ProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['own_posts'] = Post.objects.filter(
            posted_by=self.request.user.id).order_by('-created')
        return context


class GoToProfile(LoginRequiredMixin, generic.base.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        kwargs['pk'] = self.request.user.id
        self.url = '/profile/{}/'.format(kwargs['pk'])
        return super(GoToProfile, self).get_redirect_url(*args, **kwargs)
