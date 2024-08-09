# from django.db.models.signals import post_save, m2m_changed
# from django.dispatch import receiver
# from .models import User
# from community.models import Community


# @receiver(m2m_changed, sender=Community.users.through)
# def m2m_changed_join_ocds_community(sender, instance, action, **kwargs):
    # sender- the model sending the signal
    #  instance- the instance of the sender model: Community
    # created- a boolean value to tell if the receiver has acted.

    # ocds = Community.objects.filter(slug='ocds-general-community')
    # ocds.objects.add(instance)
    
    # ocds_community = Community.objects.filter(slug='ocds-general-community').prefetch_related('users')
    # users = User.objects.exclude(community=ocds_community)
    # if users:
    #     print(action)
    #     ocds_community.users.add(*users)

    # if action == 'post_add' and not reverse:
        # Check if the community slug is 'ocds-general-community'
    # if created:
    #     instance.slug = "ocds-general-community"
    #     all_users = User.objects.all()
    #     for user in all_users:
    #         instance.users.add(user)
            # Get the Community instance
    # community = Community.objects.get(slug="ocds-general-community")
    # if created:
    #     ocds = Community.objects.filter(slug='ocds-general-community')
    #     ocds.objects.add(instance)
    
    # Get all users and add them to the community
    # all_users = User.objects.all()
    # community.users.add(*all_users)