from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings


from . import models


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if not created:
        return
    profile = models.Profile(user=instance)
    profile.save()


@receiver(post_delete, sender=models.Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:
        instance.user.delete()
