from messaging.models import Message
from rest_framework.serializers import ModelSerializer


class MessageDetailSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender',
                            'sent_at',
                            'sender_deleted_at',
                            'sender_deleted_perm',
                            'recipient_deleted_at',
                            'recipient_deleted_perm',
                            'recipient_seen']
