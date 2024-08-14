# from django.db.models.signals import pre_save, post_save, m2m_changed
# from .models import CommunityMessage
# from accounts.models import User
# from django.dispatch import receiver

# @receiver(pre_save, sender=CommunityMessage)
# def pre_save_create_community_message(request, sender, instance, created, **kwargs):
#     if created:
#         user = request.user
#         if user.user_type == 'admin':