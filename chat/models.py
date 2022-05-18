from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()


class Chat(models.Model):
    members = models.ManyToManyField(User, related_name='chats')
    title = models.CharField(verbose_name='Название беседы', default="", max_length=100, null=True, blank=True)
    is_empty = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_page(self, page):
        num_of_messages_on_page = 10
        return self.messages.all().order_by('-timestamp')[num_of_messages_on_page * (page - 1): num_of_messages_on_page * page]

    def last_10_messages(self):
        return self.messages.all()[:10]

    def last_message(self):
        return self.messages.first()

    def formate_date(self):
        if datetime.now().date() == self.timestamp.date():
            return 'Today'
        elif (datetime.now() - timedelta(days=1)).date() == self.timestamp.date():
            return 'Yesterday'
        return self.timestamp.strftime('%B %d')

    def get_absolute_url(self):
        return reverse('room', args=[str(self.pk)])


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.author.username

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)
        self.chat.is_empty = False
        self.chat.timestamp = self.timestamp
        self.chat.save()

    def formate_date(self):
        if datetime.now().date() == self.timestamp.date():
            return self.timestamp.strftime('%H:%M | Today')
        elif (datetime.now() - timedelta(days=1)).date() == self.timestamp.date():
            return self.timestamp.strftime('%H:%M | Yesterday')
        return self.timestamp.strftime('%H:%M | %B %d')


    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]
