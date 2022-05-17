from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, UserInfo


class UserInfoInline(admin.StackedInline):
    model = UserInfo
    extra = 0


class CustomUserAdmin(admin.ModelAdmin):
    inlines = [UserInfoInline,]


admin.site.register(CustomUser, CustomUserAdmin)
