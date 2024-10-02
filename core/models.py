from django.db import models
from django.contrib.auth.models import User

LEVEL_SKILL = (
    ("elementary", "начальный"),
    ("Pre-Intermediate", "ниже среднего"),
    ("Intermediate", "средний"),
    ("Upper-Intermediate", "выше среднего"),
    ("Advanced", "продвинутый"),
    ("Proficiency", "профессиональный"),
)

LENGTH_LIST = (
    ('en', 'Английский'),
    ('ar', 'Арабский'),
    ('hy', 'Армянский'),
    ('bg', 'Болгарский'),
    ('hu', 'Венгерский'),
    ('vi', 'Вьетнамский'),
    ('el', 'Греческий'),
    ('da', 'Датский'),
    ('he', 'Иврит'),
    ('is', 'Исландский'),
    ('es', 'Испанский'),
    ('it', 'Итальянский'),
    ('zh', 'Китайский'),
    ('ko', 'Корейский'),
    ('lv', 'Латышский'),
    ('lt', 'Литовский'),
    ('ms', 'Малайский'),
    ('de', 'Немецкий'),
    ('nl', 'Нидерландский'),
    ('no', 'Норвежский'),
    ('fa', 'Персидский'),
    ('pl', 'Польский'),
    ('pt', 'Португальский'),
    ('ro', 'Румынский'),
    ('ru', 'Русский'),
    ('sk', 'Словацкий'),
    ('sl', 'Словенский'),
    ('th', 'Тайский'),
    ('tr', 'Турецкий'),
    ('uk', 'Украинский'),
    ('fi', 'Финский'),
    ('fr', 'Французский'),
    ('hi', 'Хинди'),
    ('cs', 'Чешский'),
    ('sv', 'Шведский'),
    ('ja', 'Японский'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)


class LengthSkill(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    length = models.CharField(max_length=30, choices=LENGTH_LIST)
    level_skill = models.CharField(max_length=30, choices=LEVEL_SKILL)


class Advertisement(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    length_to_learn  = models.CharField(max_length=30, choices=LEVEL_SKILL)
    length_level_to_learn = models.CharField(max_length=30, choices=LEVEL_SKILL)


class Lesson(models.Model):
    userA = models.ManyToManyField(UserProfile, related_name="lessons_as_userA")
    userB = models.ManyToManyField(UserProfile, related_name="lessons_as_userB")
    language_to_teach_userA = models.CharField(max_length=30)
    language_to_teach_userB = models.CharField(max_length=30)
    language_to_learn_userA = models.CharField(max_length=30)
    language_to_learn_userB = models.CharField(max_length=30)
    date_lesson = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()


