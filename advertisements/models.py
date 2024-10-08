from django.db import models
from django.contrib.auth.models import User
from constants import LANGUAGE_LIST, LEVEL_SKILL

class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language_to_learn  = models.CharField(max_length=30, choices=LANGUAGE_LIST)
    language_level_to_learn = models.CharField(max_length=30, choices=LEVEL_SKILL)