from django.contrib import admin
from .models import Message, Chat


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['author', 'chat', 'content', 'timestamp']


class MessageInline(admin.StackedInline):
    model = Message
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    inlines = [MessageInline,]
    list_display = ['timestamp', 'find_messages']

    def find_messages(self, obj):
        messages = obj.messages.all()
        return messages

    find_messages.short_description = "Messages"