from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render

from .models import Chat


User = get_user_model()


def index(request):
    return render(request, 'index.html', {})


def room(request, chat_pk):
    chat = get_object_or_404(Chat, pk=chat_pk)
    members = chat.members.all()
    if request.user in members:
        companion = members.exclude(pk=request.user.pk)[0]
        return render(request, 'chatroom.html', context={
            'room_name': chat_pk,
            'companion': companion,
        })
    else:
        response = render(request, '404.html',)
        response.status_code = 404
        return response


@login_required(login_url='login')
def create_chat(request, user_pk):
    my_user = request.user
    companion = User.objects.get(id=user_pk)
    for chat in my_user.chats.all():
        if companion in chat.members.all():
            return redirect('chat', chat_pk=chat.pk)
    new_chat = Chat()
    new_chat.save()
    new_chat.members.add(my_user.pk, companion.pk)
    return redirect('chat', chat_pk=new_chat.pk)
