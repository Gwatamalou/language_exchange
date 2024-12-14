from django.db import transaction
from django.shortcuts import get_object_or_404

import logging

from users.models import LanguageSkill

logger = logging.getLogger(__name__)

__all__ = [
    'get_current_language_skill',
    'is_skill_owner',
    'add_language_skill',
    'update_language_skill',
    'delete_skill',
]



def get_current_language_skill(skill_id):
    return get_object_or_404(LanguageSkill, id=skill_id)


def is_skill_owner(skill, user):
    if not skill.user == user:
        logger.warning(f'user {user} attempted to update someone else\'s skill')
        return False
    else:
        return True


@transaction.atomic
def add_language_skill(user, form):
    if form.is_valid():
        try:
            language_skill = form.save(commit=False)

            if not LanguageSkill.objects.filter(user=user, language=language_skill.language).exists():
                language_skill.user = user
                language_skill.save()
                logger.info(f'added is user skill {user}')
            else:
                logger.warning(f'Skill {language_skill.language} already exists for user {user}')

        except Exception as e:
            logger.error(f'error adding user skill {user} | {e}')

    else:
        logger.warning(f'skill addition form is invalid for the user {user}')


@transaction.atomic
def update_language_skill(user, form):
    if form.is_valid():
        try:
            language_skill = form.save(commit=False)

            if not LanguageSkill.objects.filter(user=user, language=language_skill.language,
                                                level_skill=language_skill.level_skill).exists():
                language_skill.save()
                logger.info(f'skill updated for user {user}')

            else:
                logger.warning(f' Duplicate skill {language_skill.language} for user {user}')

        except Exception as e:
            logger.error(f'error updating skill for user {user} | {e}')

    else:
        logger.warning(f'skill update form is invalid for user {user}')






@transaction.atomic
def delete_skill(user, skill):
    try:
        skill.delete()
        logger.info(f' skill has been deleted for the user {user}')
    except Exception as e:
        logger.error(f'Error when deleting a skill for a user {user} | {e}')
