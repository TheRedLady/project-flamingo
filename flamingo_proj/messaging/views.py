from datetime import datetime, timedelta

from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.core.serializers.json import DjangoJSONEncoder


from .models import Message
from .forms import MessageForm


@login_required
def messages_main(request):
    inbox_count = Message.objects.inbox_for(request.user).count()
    sent_count = Message.objects.outbox_for(request.user).count()
    trash_count = Message.objects.trash_for(request.user).count()
    context = {'inbox_count': inbox_count, 'sent_count': sent_count, 'trash_count': trash_count}
    return render(request, 'messaging/messages_view.html', context=context)


# @login_required
# def message_check(request):
#     threshold = timezone.now() - timedelta(minutes=5)
#     new_messages = Message.objects.filter(recipient=request.user, sent_at__gt=threshold)
#     # return JsonResponse({'new_messages': bool(new_messages)})
#     return JsonResponse({'new_messages': True})

@login_required
def message_check(request):
    temp = Message.objects.not_seen_for(request.user)
    json_val_list = temp.values_list('id', 'message_body').order_by('-sent_at')
    new_messages = json.dumps(list(json_val_list), cls=DjangoJSONEncoder)
    for message in temp:
        message.recipient_seen = True
        message.save()
    return JsonResponse({
        'new_messages': new_messages,
        'new_messages_available': bool(json_val_list),
        'new_messages_count': len(json_val_list),
    })


@login_required
def inbox(request):
    message_list = Message.objects.inbox_for(request.user)
    context = {'message_list': message_list}
    return render(request, 'display_chat.html', context=context)


@login_required
def sent(request):
    message_list = Message.objects.outbox_for(request.user)
    context = {'message_list': message_list}
    return render(request, 'display_chat.html', context=context)


@login_required
def trash(request):
    message_list = Message.objects.trash_for(request.user)
    context = {'message_list': message_list}
    return render(request, 'display_chat.html', context=context)


@login_required
def compose(request):
    if request.method == "POST":
        form = MessageForm(request.POST or None)
        form.message_body = request.POST["message_body"]
        form.recipient = request.POST["recipient"]
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, "You messaged successfully!")
            return JsonResponse({'you_sent': message.message_body,
                                 'messageId': message.id})
        else:
            messages.error(request, "You entered something wrong here!")
            return JsonResponse({'message_body': 'Error!'})

    else:
        messages.error(request, "Something went wrong with this message!")
        return JsonResponse({'message_body': 'Error!'})


def detail(request, message_id):
    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    if (message.sender != user) and (message.recipient != user):
        raise Http404

    context = {'message': message}
    return render(request, "message.html", context=context)


def delete_message(request, message_id):
    now = timezone.now()
    deleted_message = get_object_or_404(Message, id=message_id)
    deleted = False
    if deleted_message.sender == request.user:
        deleted = True
        if deleted_message.sender_deleted_at is None:
            deleted_message.sender_deleted_at = now
        else:
            deleted_message.sender_deleted_perm = True
    if deleted_message.recipient == request.user:
        deleted = True
        if deleted_message.recipient_deleted_at is None:
            deleted_message.recipient_deleted_at = now
        else:
            deleted_message.recipient_deleted_perm = True
    if deleted_message.for_delete():
        deleted_message.delete()
        return redirect('messages:trash')
    elif deleted:
        deleted_message.save()
        messages.success(request, "Message deleted successfully.")
        return redirect('messages:inbox')
    else:
        raise Http404("You cannot delete this message!")


def messaging(request):
    return render(request, 'messaging/messagesKO.html', context={})
