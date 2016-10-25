from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.http import JsonResponse


from .forms import PostForm
from .models import Post, Tag, Like, Share


class PostView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        Post.add_liked_by_user([self.object], self.request.user)
        Post.add_shared_property([self.object])
        context['post'] = context['object']
        return context


@login_required
def posts_by_tag(request, tag):
    requested_tag = Tag.objects.get(tag='#' + tag)
    posts = Post.objects.filter(tag=requested_tag).order_by('-created')
    Post.add_shared_property(posts)
    context = {
        "tag": tag,
        "posts": Post.add_liked_by_user(posts, request.user)
    }
    return render(request, 'posts/tagKO.html', context)


@login_required
def trending(request):
    context = {'trending': Tag.get_trending()}
    return render(request, 'posts/trending.html', context)
