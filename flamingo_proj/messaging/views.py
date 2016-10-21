from django.shortcuts import render


def messaging(request):
    return render(request, 'messaging/messagesKO.html', context={})
