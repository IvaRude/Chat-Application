from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, UserInfo
from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    model = CustomUser
    # fields = ['username', 'password']
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(DetailView):
    model = UserInfo
    template_name = 'accounts/profile.html'


class UsersListView(ListView):
    model = CustomUser
    template_name = 'accounts/all_users.html'