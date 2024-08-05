
VOTE_CHOICES = (
        ('UPVOTE', 'upvote'),
        ('DOWNVOTE', 'downvote'),
    )


from django.db.models import TextChoices

class VoteChoices(TextChoices):
    UPVOTE = "Upvote"
    DOWNVOTE = 'Downvote'