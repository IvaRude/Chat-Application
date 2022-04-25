from django.urls import path, include
from django.contrib.auth.views import LoginView

from .views import (SignUpView, ProfileView)


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
]