from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import UserProfile, Users


@receiver(post_save, sender=Users)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)