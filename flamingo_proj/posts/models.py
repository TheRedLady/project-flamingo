from __future__ import unicode_literals
import re
from collections import Counter

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Post(TimeStampedModel):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(max_length=1000, editable=True)

    def get_hash_tags(self):
        return set(re.findall(r'(?<![\w\d])#[a-zA-Z0-9]+(?![\w\d])', self.content))

    def split_by_hashtag(self):
        return re.split(r'((?<![\w\d])#[a-zA-Z0-9]+(?![\w\d]))', self.content)

    def create_hashtags(self):
        old_refs = self.tag_set.all()
        hash_tags = self.get_hash_tags()
        split_content = self.split_by_hashtag()
        for t in hash_tags:
            # Adding the new tags
            obj, created = Tag.objects.get_or_create(tag=t)
            obj.posts.add(self)
            obj.save()
            tag_link = reverse('posts:tag', kwargs={'tag': t[1:]})
            for index, elem in enumerate(split_content):
                if elem == t:
                    split_content[index] = '<a href="{}">{}</a>'.format(tag_link, t)
        result_content = ''.join(split_content)
        this_instance = Post.objects.filter(id=self.id)
        this_instance.update(content=result_content)

        old_refs = old_refs.exclude(tag__in=hash_tags)
        for old in old_refs:
            old.posts.remove(self)
            old.save()
        self.refresh_from_db()

    @staticmethod
    def add_shared_property(set_of_posts):
        for post in set_of_posts:
            try:
                post.shared = Share.objects.get(shared_post_id=post.id)
            except Share.DoesNotExist:
                post.shared = None

    @staticmethod
    def add_liked_by_user(set_of_posts, user):
        for post in set_of_posts:
            try:
                Like.objects.get(liked_by=user, post=post)
                post.liked_by_user = True
            except Like.DoesNotExist:
                post.liked_by_user = False
        return set_of_posts

    def __str__(self):
        return "Post by {}, posted on {}".format(self.posted_by.get_full_name(), self.created.date())

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.id})

    @classmethod
    def get_latest(cls):
        return cls.objects.order_by('-created')[:100]


@python_2_unicode_compatible
class Share(TimeStampedModel):
    original_post = models.ForeignKey(Post, related_name="original")
    shared_post = models.ForeignKey(Post)

    def __str__(self):
        return "Shared by {}".format(self.shared_post.posted_by.get_full_name())


@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=30, unique=True)
    posts = models.ManyToManyField(Post)

    @classmethod
    def get_trending(cls):
        latest_posts = Post.get_latest()
        tags_found = [tag for post in latest_posts for tag in post.tag_set.all()]
        tag_counts = Counter(tags_found).most_common(5)
        return [t[0] for t in tag_counts]

    def __str__(self):
        return "Tag {}".format(self.tag)

    def get_absolute_url(self):
        return reverse('posts:tag', kwargs={'tag': self.tag[1:]})

    def get_occurrences(self):
        return self.posts.all().count()


@python_2_unicode_compatible
class Like(models.Model):
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post, related_name='likes')

    def __str__(self):
        return "{} likes {}".format(self.liked_by, self.post)
