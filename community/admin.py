from django.contrib import admin
from .models import Community, Information
# Register your models here.


@admin.register(Community)
class Community(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'slug']
    list_filter = ['name']
    prepopulated_fields = {"slug": ("name",)}