from django.db import models
from django.contrib.auth.models import User
from constants import LANGUAGE_LIST, LEVEL_SKILL

class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    language_to_learn  = models.CharField(max_length=30, choices=LANGUAGE_LIST)
    language_level_to_learn = models.CharField(max_length=30, choices=LEVEL_SKILL)
    data = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-data',)

class Notification(models.Model):
    responder = models.ForeignKey(User, related_name='responder', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    room = models.CharField(max_length=150, default='None')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['responder', 'user', 'advertisement'], name='unique_notification')
        ]


    def __str__(self):
        return f"Notification for {self.user.username} about from {self.responder.username}"