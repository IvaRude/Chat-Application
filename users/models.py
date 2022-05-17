from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login
from annoying.fields import AutoOneToOneField
import os

# from chats.models import Chat

# def avatar_upload_to(instance, filename):
#     return os.path.join(MEDIA_ROOT, instance.user.username + os.path.splitext(filename)[1])


# class PostAuthor(models.Model):
#     pass


class CustomUser(AbstractUser):
    def get_name(self):
        first_name = self.user_info.first_name
        last_name = str(self.user_info.last_name)
        if first_name or last_name:
            return ' '.join([first_name, last_name]).strip()
        return self.username

class UserInfo(models.Model):
    user = AutoOneToOneField(CustomUser, related_name='user_info', on_delete=models.CASCADE, null=False)
    first_name = models.CharField(max_length=30, verbose_name='Имя', default='')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия', default='')
    # birth_date = models.DateField(
    #     verbose_name='Дата рождения', null=True, blank=True)
    # age = models.PositiveIntegerField(null=True, blank=True)

    def get_absolute_url(self):
        """ нужен, чтобы при создании очередного объекта сразу перебрасывало на эту страницу
        без get_success_url """
    
        return reverse('profile', args=[str(self.pk)])
