from django.db import models
from accounts.models import User
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _


# potential tables tags and vote
class Question(models.Model):
    owner = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    body = models.CharField(max_length=250, null=True)
    # slug = models.SlugField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    tags = TaggableManager()

    def __str__(self):
        return f"{self.body}"


class Reply(models.Model):
    question = models.ForeignKey(Question, related_name='replies', on_delete=models.CASCADE)
    body = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    question = models.ForeignKey(Question, related_name='votes', on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, related_name='replies', on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, related_name='vote', on_delete=models.DO_NOTHING)


# class Tag(models.Model):
#     class TagOptions(models.TextChoices):
#         FRONTEND = "FRONTEND", _("Frontend")
#         BACKEND = "BACKEND", _("Backend")
#         UI_DESIGN = "UI-DESIGN", _("Ui_design")
#         PRODUCT_MANAGEMENT = "PRODUCT_MANAGEMENT", _("Product_management")
#         TECH_CAREER = "TECH_CAREER", _("Tech_career")

#     questions = models.ForeignKey(Question, related_name='tags', on_delete=models.DO_NOTHING)
#     slug = models.SlugField(max_length=200, unique=True)
#     options = models.CharField(choices=TagOptions, default=TagOptions.TECH_CAREER)


