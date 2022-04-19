from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # list_display = ['user', 'date_of_birth', 'photo']
    pass