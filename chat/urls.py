from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:chat_pk>/', views.room, name='room'),
]
