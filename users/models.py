from django.db import models
from django.contrib.auth.models import User

from constants import LANGUAGE_LIST, LEVEL_SKILL




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/', blank=True, null=True, default='images/default.png')


    def get_absolute_url(self):
        pass


class LanguageSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=30, choices=LANGUAGE_LIST, default='')
    level_skill = models.CharField(max_length=30, choices=LEVEL_SKILL, default='')