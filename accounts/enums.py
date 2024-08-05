from django.db import models

class UserType(models.TextChoices):
        STUDENT = "student"
        MENTOR = "mentor"
        ADMIN = "admin"