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


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST or None)
        form.content = request.POST["content"]
        if form.is_valid():
            instance = form.save(commit=False)
            instance.posted_by = request.user
            instance.save()
            messages.success(request, "You posted successfully!")
            return JsonResponse({'you_posted': instance.content,
                                 'postId': instance.id})
    else:
        messages.error(request, "Something went wrong this your post!")
        return JsonResponse({'you_posted': "Error!"})


@login_required
def like(request, id):
    if request.method == 'GET':
        try:
            Like.objects.get(
                liked_by=request.user,
                post=Post.objects.get(id=id))
            return JsonResponse({'liked_by_user': True})
        except Like.DoesNotExist:
            return JsonResponse({'liked_by_user': False})

    elif request.method == 'POST':
        obj, created = Like.objects.get_or_create(
            liked_by=request.user,
            post=Post.objects.get(id=id),
        )
        if not created:
            obj.delete()
            return JsonResponse({'liked_by_user': False})
        else:
            return JsonResponse({'liked_by_user': True})


@login_required
def posts_by_tag(request, tag):
    requested_tag = Tag.objects.get(tag='#' + tag)
    posts = Post.objects.filter(tag=requested_tag).order_by('-created')
    Post.add_shared_property(posts)
    context = {
        "tag": tag,
        "posts": Post.add_liked_by_user(posts, request.user)
    }
    return render(request, 'posts/tag.html', context)


@login_required
def post_edit(request, id):
    instance = get_object_or_404(Post, id=id)
    if request.user.id == instance.posted_by.id:
        form = PostForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "You have successfully edited this post!")
            return redirect('profiles:go-to-profile')
        context = {
            'instance': instance,
            'form': form
        }
        return render(request, 'posts/post_form.html', context)
    else:
        raise Http404("You can only edit your own posts!")


def post_delete(request, id):
    instance = get_object_or_404(Post, id=id)
    if request.user.id == instance.posted_by.id:
        instance.delete()
        messages.success(request, "You have successfully deleted this post!")
        return redirect('profiles:go-to-profile')
    else:
        raise Http404("You can only delete your own posts")


def post_share(request, id):
    if request.method == "POST":
        instance = get_object_or_404(Post, id=id)
        share = Post.objects.create(posted_by=request.user, content=instance.content)
        Share.objects.create(original_post_id=id, shared_post_id=share.id)
        Post.add_shared_property([share])
        messages.success(request, "You have successfully shared this post!")
        return JsonResponse({'postId': share.id})
    else:
        messages.error(request, "Something went wrong!")
        return JsonResponse({'you_posted': "Error!"})


def trending(request):
    context = {'trending': Tag.get_trending()}
    return render(request, 'posts/trending.html', context)
