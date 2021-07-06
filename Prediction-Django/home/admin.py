from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from home.models import CustomUser


class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)
