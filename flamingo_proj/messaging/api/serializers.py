from messaging.models import Message
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class MessageDetailSerializer(ModelSerializer):
    sender_name = SerializerMethodField()
    recipient_name = SerializerMethodField()

    def get_sender_name(self, obj):
        return obj.sender.get_full_name()

    def get_recipient_name(self, obj):
        return obj.recipient.get_full_name()

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender_name',
                            'recipient_name',
                            'sender',
                            'sent_at',
                            'sender_deleted_at',
                            'sender_deleted_perm',
                            'recipient_deleted_at',
                            'recipient_deleted_perm',
                            'recipient_seen']
