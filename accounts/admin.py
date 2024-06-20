from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_login', 'first_name', 'last_name', 'email', 'username', 'user_type', 'is_active', 'date_of_birth', 'phone_number')
    list_filter = ('first_name', 'last_name', 'user_type', 'is_active', 'is_superuser')
    search_fields = ['id', 'last_login', 'first_name', 'last_name', 'username']