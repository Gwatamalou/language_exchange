from django.db import transaction
from django.shortcuts import get_object_or_404

from users.models import LanguageSkill

__all__ = [
    'get_current_language_skill',
    'is_skill_owner',
    'add_language_skill',
    'update_language_skill',
    'delete_skill',
]



def get_current_language_skill(skill_id):
    """возвращает данные о выбранном языке и уровне владения"""
    return get_object_or_404(LanguageSkill, id=skill_id)


def is_skill_owner(skill, user):
    """Проверка, является ли пользователь владельцем навыка"""
    return skill.user == user


@transaction.atomic
def add_language_skill(user, form):
    if form.is_valid():
        language_skill = form.save(commit=False)
        if not LanguageSkill.objects.filter(user=user, language=language_skill.language).exists():
            language_skill.user = user
            language_skill.save()
        # else:
        #     logger.warning(f'Skill {language_skill.language} already exists for user {user}')


@transaction.atomic
def update_language_skill(user, form):
    """Обновление языкового навыка"""
    if form.is_valid():
        language_skill = form.save(commit=False)
        if not LanguageSkill.objects.filter(user=user, language=language_skill.language,
                                            level_skill=language_skill.level_skill).exists():
            language_skill.save()
        # else:
        #     logger.warning(f' Duplicate skill {language_skill.language} for user {user}')


@transaction.atomic
def delete_skill(skill):
    skill.delete()
