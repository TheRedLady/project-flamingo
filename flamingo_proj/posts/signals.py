from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_POST_MODEL)
def create_tags(sender, instance, created, **kwargs):
    instance.create_hashtags()
