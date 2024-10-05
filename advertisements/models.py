from django.db import models
from users.models import UserProfile
from constants import LEVEL_SKILL

class Advertisement(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    language_to_learn  = models.CharField(max_length=30, choices=LEVEL_SKILL)
    language_level_to_learn = models.CharField(max_length=30, choices=LEVEL_SKILL)