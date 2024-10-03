from django.db import models
from django.contrib.auth.models import User
from constants import LENGTH_LIST, LEVEL_SKILL


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)


class LengthSkill(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    length = models.CharField(max_length=30, choices=LENGTH_LIST)
    level_skill = models.CharField(max_length=30, choices=LEVEL_SKILL)