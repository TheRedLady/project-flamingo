from messaging.models import Message
from .serializers import MessageDetailSerializer

from rest_framework.viewsets import ModelViewSet


class MessageViewSet(ModelViewSet):
    serializer_class = MessageDetailSerializer

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
            queryset = Message.objects.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
