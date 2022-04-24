from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login
import os


# def avatar_upload_to(instance, filename):
#     return os.path.join(MEDIA_ROOT, instance.user.username + os.path.splitext(filename)[1])


# class PostAuthor(models.Model):
#     pass


class CustomUser(AbstractUser):
    pass


class UserInfo(models.Model):
    user = models.OneToOneField(CustomUser, related_name='user_info', on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия', null=True, blank=True)
    # birth_date = models.DateField(
    #     verbose_name='Дата рождения', null=True, blank=True)
    # age = models.PositiveIntegerField(null=True, blank=True)

    # def get_absolute_url(self):
    #     """ нужен, чтобы при создании очередного объекта сразу перебрасывало на эту страницу
    #     без get_success_url """
    #
    #     return reverse('profile', args=[str(self.id)])
