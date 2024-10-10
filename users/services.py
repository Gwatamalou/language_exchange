from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from users.models import LanguageSkill


def register_user(form):
    if form.is_valid():
        return form.save()
    return None


def _get_user(user_id):
    """Получение данных о пользователе из бд"""
    return get_object_or_404(User, id=user_id)


def _get_user_language(user_id):
    """Получение данных о языках и уровнях владения из бд"""
    return LanguageSkill.objects.filter(user_id=user_id)


def get_user_data(user_id):
    return _get_user(user_id), _get_user_language(user_id)