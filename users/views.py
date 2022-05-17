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


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UserInfo
    template_name = 'accounts/profile.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user == self.get_object().user


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserInfo
    fields = ['first_name', 'last_name']
    template_name = 'accounts/edit.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user == self.get_object().user


class UsersListView(ListView):
    model = CustomUser
    template_name = 'accounts/all_users.html'