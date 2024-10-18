from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from advertisements.models import Notification
from users.models import UserProfile


@receiver(post_save, sender=Notification)
def my_callback(sender, instance, created, **kwargs):
    if created:
            print(instance.user.username)
            print(f"добавлено уведомления")

            @receiver(post_save, sender=User)
            def create_user_profile(sender, instance, created, **kwargs):
                if created:
                    UserProfile.objects.create(user=instance)