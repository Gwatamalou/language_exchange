from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from advertisements.models import Notification
from users.models import LanguageSkill


def register_user(form):
    if form.is_valid():
        return form.save()
    return None


def get_object_or_error(model, **kwargs):
    """Получение данных или страницы 404"""
    return get_object_or_404(model, **kwargs)


def get_object_if_any(model, **kwargs):
    """Получение данных если есть"""
    return model.objects.filter(**kwargs)


def get_user_data(user_id):
    """возвращает данный пользователя"""
    return get_object_or_error(User, id=user_id), get_object_if_any(LanguageSkill, user_id=user_id)


def add_language_skill(user, form):
    if form.is_valid():
        language_skill = form.save(commit=False)
        language_skill.user = user
        language_skill.save()
        return language_skill
    return None


def get_current_language(skill_id):
    """возвращает данные о выбранном языке и уровне владения"""
    return get_object_or_error(LanguageSkill, id=skill_id)

def update_language_skill(form):
    """Обновление языкового навыка"""
    if form.is_valid():
        return form.save()
    return None

def check_skill_owner(skill, user):
    """Проверка, является ли пользователь владельцем навыка"""
    return skill.user == user

def get_notification(user_id):
    return get_object_if_any(Notification, user_id=user_id)
