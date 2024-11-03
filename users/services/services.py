from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from advertisements.models import Notification
from users.models import LanguageSkill, UserProfile

__all__ = ['get_user_data',
           'register_user',
           'get_current_language',
           'check_skill_owner',
           'get_notification',
           'get_object_or_error',
           'get_object_if_any',
           'create_new_user',
           'add_language_skill',
           'update_language_skill'
           ]


def _extract_user_data(user_id):
    return get_object_or_404(User, id=user_id)


def _extract_user_languages_skill(user_id):
    return LanguageSkill.objects.filter(user_id=user_id)


def _extract_avatar_url(user_id):
    user_profile = UserProfile.objects.get(user_id=user_id)
    return user_profile.avatar.url


def create_new_user(user):
    UserProfile.objects.create(user=user)


def add_language_skill(user, form):
    if form.is_valid():
        language_skill = form.save(commit=False)
        if not LanguageSkill.objects.filter(user=user, language=language_skill.language).exists():
            language_skill.user = user
            language_skill.save()


def update_language_skill(user, form):
    """Обновление языкового навыка"""
    if form.is_valid():
        language_skill = form.save(commit=False)
        if not LanguageSkill.objects.filter(user=user, language=language_skill.language,
                                            level_skill=language_skill.level_skill).exists():
               language_skill.save()


def get_current_language(skill_id):
    """возвращает данные о выбранном языке и уровне владения"""
    return get_object_or_404(LanguageSkill, id=skill_id)


def check_skill_owner(skill, user):
    """Проверка, является ли пользователь владельцем навыка"""
    return skill.user == user



def delete_skill(skill):
    skill.delete()


def update_avatar(profile, avatar):
    profile.avatar = avatar
    profile.save()



def get_user_data(user_id):
    return _extract_user_data(user_id), _extract_user_languages_skill(user_id), _extract_avatar_url(user_id)


def register_user(form):
    if form.is_valid():
        return form.save()
    return None


def get_notification(user_id):
    return Notification.objects.filter(user_id=user_id)


def get_current_notification(notification_id, user):
    return Notification.objects.get(id=notification_id, user=user)


def notification_accept(notification):
    room = notification.room
    notification.delete()
    return room


def notification_delete(notification):
    notification.delete(notification)


def get_object_or_error(model, **kwargs):
    """Получение данных или страницы 404"""
    return get_object_or_404(model, **kwargs)


def get_object_if_any(model, **kwargs):
    """Получение данных если есть"""
    return model.objects.filter(**kwargs)

