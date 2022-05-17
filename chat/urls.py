from django.urls import path

from . import views

urlpatterns = [
    path('<int:chat_pk>/', views.room, name='room'),
    path('create_chat/<int:user_pk>/', views.create_chat, name='create_chat'),
]
