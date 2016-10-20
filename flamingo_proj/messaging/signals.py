from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_MESSAGING_MODEL)
def delete_permanent(sender, instance, created, **kwargs):
    if instance.sender_deleted_perm and instance.recipient_deleted_perm:
        instance.delete()


