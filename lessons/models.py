from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    userA = models.ManyToManyField(User, related_name="lessons_as_userA")
    userB = models.ManyToManyField(User, related_name="lessons_as_userB")
    language_to_teach_userA = models.CharField(max_length=30)
    language_to_teach_userB = models.CharField(max_length=30)
    language_to_learn_userA = models.CharField(max_length=30)
    language_to_learn_userB = models.CharField(max_length=30)
    date_lesson = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()


