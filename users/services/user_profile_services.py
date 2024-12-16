from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction

import logging

from users.models import LanguageSkill, UserProfile

logger = logging.getLogger(__name__)

__all__ = ['get_all_user_data',
           'get_user_data',
           'register_user',
           'update_avatar',
           ]



def get_user_data(user_id: int):
    return User.objects.select_related('userprofile').get(id=user_id)


def get_user_language_skills(user_id: int):
    try:
        return LanguageSkill.objects.filter(user_id=user_id).order_by('language')
    except Exception as e:
        logger.warning(f'failed to connect to the database {e}')
        return None


def get_user_avatar_url(user_id: int):
    try:
        user_profile = UserProfile.objects.get(user_id=user_id)
        return user_profile.avatar.url
    except Exception as e:
        logger.warning(f'failed to connect to the database {e}')
        return None



def get_all_user_data(user_id: int):
    return get_user_data(user_id), get_user_language_skills(user_id), get_user_avatar_url(user_id)


@transaction.atomic
def update_avatar(user, profile, avatar):
    if avatar.size > 8 * 1024 * 1024:
        logger.info('file size greater than 8mb ')
        return
    try:
        profile.avatar = avatar
        profile.save()
        logger.info(f'add new avatar for {user}')
    except Exception as e:
        logger.error(f'error add new avatar for user {user} | {e}')




@transaction.atomic
def register_user(form, user):
    try:
        form.save()
        logger.info(f'created user {user} successfully')
    except Exception as e:
        logger.warning(f'user creation error {user} | {e}')


