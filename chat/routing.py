from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_pk>\w+)/$', consumers.ChatRoomConsumer.as_asgi(), name='chatSocket'),
    re_path(r'ws/user/(?P<username>\w+)/$', consumers.SideBarConsumer.as_asgi(), name='sidebarSocket'),
]