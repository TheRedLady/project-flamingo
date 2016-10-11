from __future__ import unicode_literals

from collections import defaultdict

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone


class MessageManager(models.Manager):

    def inbox_for(self, user):
        return self.filter(recipient=user, recipient_deleted_at__isnull=True).order_by('-sent_at')

    def outbox_for(self, user):
        return self.filter(sender=user, sender_deleted_at__isnull=True).order_by('-sent_at')

    def trash_for(self, user):
        return (self.filter(recipient=user,
                            recipient_deleted_at__isnull=False,
                            recipient_deleted_perm=False) | \
                self.filter(sender=user,
                            sender_deleted_at__isnull=False,
                            sender_deleted_perm=False)).order_by('-sent_at')

    def not_seen_for(self, user):
        return self.filter(recipient=user, recipient_seen=False, recipient_deleted_at__isnull=True)


@python_2_unicode_compatible
class Message(models.Model):
    message_body = models.TextField(max_length=300)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_messages")
    sent_at = models.DateTimeField("sent at", null=True, blank=True)
    sender_deleted_at = models.DateTimeField(null=True, blank=True)
    sender_deleted_perm = models.BooleanField(default=False)
    recipient_deleted_at = models.DateTimeField(null=True, blank=True)
    recipient_deleted_perm = models.BooleanField(default=False)
    recipient_seen = models.BooleanField(default=False)

    objects = MessageManager()

    def __str__(self):
        return str(self.sender) + ', ' + str(self.recipient)

    def get_absolute_url(self):
        pass

    def save(self, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()
        super(Message, self).save(**kwargs)

    def for_delete(self):
        return self.sender_deleted_perm and self.recipient_deleted_perm

    class Meta:
        ordering = ['-sent_at']
