from django.db import models
from django.contrib.auth.models import User
from constants import LEVEL_SKILL

class Advertisement(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    language_to_learn  = models.CharField(max_length=30, choices=LEVEL_SKILL)
    language_level_to_learn = models.CharField(max_length=30, choices=LEVEL_SKILL)