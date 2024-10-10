from django.db import models
from django.contrib.auth.models import User
from constants import LANGUAGE_LIST, LEVEL_SKILL

class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    language_to_learn  = models.CharField(max_length=30, choices=LANGUAGE_LIST)
    language_level_to_learn = models.CharField(max_length=30, choices=LEVEL_SKILL)


class Notification(models.Model):
    responder = models.ForeignKey(User, related_name='responder', on_delete=models.CASCADE)  # Пользователь, откликнувшийся на объявление
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, которому отправлено уведомление
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)  # Соответствующее объявление
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')), default='pending')  # Статус отклика

    def __str__(self):
        return f"Notification for {self.user.username} about {self.advertisement.title} from {self.responder.username}"