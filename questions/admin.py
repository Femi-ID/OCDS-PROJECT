from django.contrib import admin
from .models import Question, Reply


@admin.register(Question)
class Question(admin.ModelAdmin):
    list_display = ['owner', 'body', 'created_at', 'tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    

