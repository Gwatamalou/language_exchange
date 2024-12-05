from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction

from users.models import LanguageSkill, UserProfile

__all__ = ['get_user_data',
           'register_user',
           'update_avatar',
           ]



def _get_user_data(user_id):
    return get_object_or_404(User, id=user_id)


def _get_user_language_skills(user_id):
    return LanguageSkill.objects.filter(user_id=user_id).order_by('language')


def _get_user_avatar_url(user_id):
    user_profile = UserProfile.objects.get(user_id=user_id)
    return user_profile.avatar.url


def get_user_data(user_id):
    return _get_user_data(user_id), _get_user_language_skills(user_id), _get_user_avatar_url(user_id)


@transaction.atomic
def update_avatar(profile, avatar):
    if avatar.size > 8 * 1024 * 1024:
        raise ValidationError('file size is too big')
    profile.avatar = avatar
    profile.save()




@transaction.atomic
def register_user(form):
     form.save()



