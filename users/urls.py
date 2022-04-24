from django.urls import path, include
from django.contrib.auth.views import LoginView

from .views import (SignUpView,)


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login')
]