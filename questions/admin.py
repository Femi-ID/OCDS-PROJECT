from django.contrib import admin
from .models import Question, Reply

@admin.register(Question)
class Question(admin.ModelAdmin):
    list_display = ['id', 'owner', 'title', 'body', 'created_at', 'tag_list']
    prepopulated_fields = {"slug": ("title",)}

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    

@admin.register(Reply)
class Reply(admin.ModelAdmin):
    list_display = ['question', 'body', 'created_at']

# @admin.register(Vote)
# class Vote(admin.ModelAdmin):
#     list_display = ['question', 'reply', 'voted_by', 'vote_type']    