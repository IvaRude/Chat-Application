from django.contrib import admin
from .models import Message, Chat


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'chat', 'content', 'timestamp']
    pass


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['timestamp',]
    pass


# admin.site.register(Chat)