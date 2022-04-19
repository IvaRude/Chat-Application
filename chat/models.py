from django.db import models
from django.utils import timezone
# from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model
import datetime

tomorrow = datetime.datetime.now()

User = get_user_model()


# class Chat(models.Model):
#     members = models.ManyToManyField(User, related_name='chats')
#     title = models.CharField(verbose_name='Название беседы', default="", max_length=100, null=True, blank=True)

#     def get_absolute_url(self):
#         return reverse('chat', {'chat_id': self.pk})


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]
