from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Chat


User = get_user_model()


def index(request):
    return render(request, 'index.html', {})


@login_required(login_url='login')
def room(request, chat_pk):
    chat = get_object_or_404(Chat, pk=chat_pk)
    members = chat.members.all()
    if request.user in members:
        companion = members.exclude(pk=request.user.pk)[0]
        # messages = chat.messages.all()
        # paginator = Paginator(messages, 10)
        # page = request.GET.get('page')
        # try:
        #     messages = paginator.page(page)
        # except PageNotAnInteger:
        #     # Если переданная страница не является числом, возвращаем первую.
        #     messages = paginator.page(1)
        # except EmptyPage:
        #     # if request.is_ajax():
        #         # Если получили AJAX-запрос с номером страницы, большим, чем их количество,
        #         # возвращаем пустую страницу.
        #         # return HttpResponse('')
        #     # Если номер страницы больше, чем их количество, возвращаем последнюю.
        #     messages = paginator.page(paginator.num_pages)
        # # if request.is_ajax():
        # #     return render(request,'chatroom.html', context={
        # #         'room_name': chat_pk,
        # #         'companion': companion,
        # #         'messages': messages
        # #     })
        return render(request, 'chatroom.html', context={
            'room_name': chat_pk,
            'companion': companion,
            # 'messages': messages
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
            return redirect('room', chat_pk=chat.pk)
    new_chat = Chat()
    new_chat.save()
    new_chat.members.add(my_user.pk, companion.pk)
    return redirect('room', chat_pk=new_chat.pk)


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если переданная страница не является числом, возвращаем первую.
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # Если получили AJAX-запрос с номером страницы, большим, чем их количество,
            # возвращаем пустую страницу.
            return HttpResponse('')
        # Если номер страницы больше, чем их количество, возвращаем последнюю.
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,'images/image/list_ajax.html',
        {'section': 'images', 'images': images})
    return render(request,'images/image/list.html',
    {'section': 'images', 'images': images})