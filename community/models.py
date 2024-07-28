from django.db import models
from accounts.models import User
import uuid

class Community(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    users = models.ManyToManyField(User)
    slug = models.SlugField(max_length=200, unique=True, null=True)

    def __str__(self):
        return f'Name: {self.name} >> Description: {self.description[:20]}'


class Information(models.Model):
    owner = models.ForeignKey(User, related_name='information', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=150)
    content = models.TextField(max_length=200)
    # image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Title: {self.title}'