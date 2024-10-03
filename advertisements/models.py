from django.db import models
from users.models import UserProfile
from constants import LEVEL_SKILL

class Advertisement(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    length_to_learn  = models.CharField(max_length=30, choices=LEVEL_SKILL)
    length_level_to_learn = models.CharField(max_length=30, choices=LEVEL_SKILL)