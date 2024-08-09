from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import User
from community.models import Community

@receiver(post_save, sender=User)
def post_save_join_ocds_community(sender, instance, created, **kwargs):
    # sender- the model sending the signal
    #  instance- the instance of the sender model: User
    # created- a boolean value to tell if the receiver has acted.
    if created:
        print('post_save', post_save)
        # if action == 'post_add':
        ocds = Community.objects.get(slug='ocds-general-community')
        ocds.users.add(instance) 
        ocds.save()