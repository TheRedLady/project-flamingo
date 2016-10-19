from messaging.models import Message
from .serializers import MessageDetailSerializer

from django.utils import timezone
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class MessageViewSet(ModelViewSet):
    serializer_class = MessageDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        folder = self.request.query_params.get('folder', None)
        if folder is not None:
            if folder == 'Sent':
                queryset = Message.objects.outbox_for(self.request.user)
            elif folder == 'Inbox':
                queryset = Message.objects.inbox_for(self.request.user)
            elif folder == 'Trash':
                queryset = Message.objects.trash_for(self.request.user)
            else:
                queryset = Message.objects.none()
        else:
            queryset = Message.objects.filter(Q(recipient_id=self.request.user) | Q(sender_id=self.request.user))
        return queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def perform_destroy(self, instance):
        user_id = self.request.user.id

        # If you are the recipient
        if instance.recipient_id == user_id:
            if instance.recipient_deleted_at is None:
                instance.recipient_deleted_at = timezone.now()
                instance.save()
            else:
                instance.recipient_deleted_perm = True
                instance.save()

        # If you are the sender
        if instance.sender_id == user_id:
            if instance.sender_deleted_at is None:
                instance.sender_deleted_at = timezone.now()
                instance.save()
            else:
                instance.sender_deleted_perm = True
                instance.save()
