from django.db import models
from accounts.models import User
from django.db.models import Sum, Q, Count
from community.models import Community
import uuid
from django.urls import reverse

from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

# potential tables tags and vote
class Question(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  primary_key=True, editable=False, unique=True)
    owner = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, blank=False)
    body = models.TextField(max_length=500, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    community = models.ForeignKey(Community, related_name='questions', on_delete=models.CASCADE, null=True, blank=False)

    tags = TaggableManager(through=UUIDTaggedItem)

    def __str__(self):
        return f"{self.owner}: {self.title[:20]}...."

    def total_votes(self):
        up_votes = self.objects.filter('votes__vote_type'=='UPVOTE').annotate(
            up_votes_sum=Count('vote_type'))
        down_votes = self.objects.filter('votes__vote_type'=='DOWNVOTE').annotate(
            down_votes_sum=Count('vote_type'))
        return (up_votes, down_votes)
    
    def get_absolute_url(self):
        return reverse("question_list", kwargs={'slug': self.slug})


class Reply(models.Model):
    question = models.ForeignKey(Question, related_name='replies', on_delete=models.CASCADE)
    body = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Vote(models.Model):
    VOTE_CHOICES = (
        ('UPVOTE', 'upvote'),
        ('DOWNVOTE', 'downvote'),
    )
    question = models.ForeignKey(Question, related_name='votes', on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, related_name='votes', on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, related_name='votes', on_delete=models.DO_NOTHING)
    vote_type = models.CharField(choices=VOTE_CHOICES, null=True)

    # def total_votes(self):
    #         return self.vote_type.aggregate(
    #             upvote=Sum('id', filter=Q(vote_type='UPVOTE')),
    #             downvote=Sum('id', filter=Q(vote_type='DOWNVOTE')),
    #             )

    

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


