from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.shortcuts import redirect

from advertisements.models import Notification



@receiver(post_save, sender=Notification)
def my_callback(sender, instance, created, **kwargs):
    if created:
            print(instance.user.username)
            print(f"добавлено уведомления")