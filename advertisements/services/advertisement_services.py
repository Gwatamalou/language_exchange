from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Case, When, IntegerField
from advertisements.models import Advertisement, Notification

import logging

from users.models import LanguageSkill


logger = logging.getLogger(__name__)


__all__ = [
    'get_current_advertisement',
    'add_new_advertisement',
    'add_new_notification',
    'get_ads',
    'get_order_language_skill',
    'get_avatar_url',
    'get_user_language_skills'
]


def get_current_advertisement(slug_id):
    """Возвращает выбранное объявление"""
    return get_object_or_404(Advertisement, id=slug_id)


def add_new_advertisement(user, form):
    """Добавляет новое объявление в БД"""
    if form.is_valid():
        try:
            advertisement = form.save(commit=False)
            if not Advertisement.objects.filter(user=user, language_to_learn=advertisement.language_to_learn,
                                                language_level_to_learn=advertisement.language_level_to_learn).exists():
                advertisement.user = user
                advertisement.save()

        except Exception as e:
            logger.error(f'Failed to create new ad for user {user} | {e}')


def add_new_notification(user, ads):
    """Создает уведомление по выбранному объявлению"""
    try:
        if not Notification.objects.filter(responder=user, user=ads.user, advertisement=ads).exists():
            Notification.objects.create(
                responder=user,
                user=ads.user,
                advertisement=ads,
                room=f'{user}{ads.user.username}',
            )
    except Exception as e:
        logger.error(f'failed to create notification | {e}')


def get_ads(user_id, slug):
    try:
        if slug == 'all':
            return Advertisement.objects.exclude(user_id=user_id).select_related('user')
        elif slug == 'my':
            return Advertisement.objects.filter(user_id=user_id).select_related('user')
    except Exception as e:
        logger.warning(f'failed to connect to the database {e}')




def get_order_language_skill(ads):
    level_order = {
        "профессиональный": 6,
        "продвинутый": 5,
        "выше среднего": 4,
        "средний": 3,
        "ниже среднего": 2,
        "начальный": 1,
    }
    try:
        return LanguageSkill.objects.filter(user__in=ads.values_list('user', flat=True)).annotate(
            level_ordering=Case(
                *[When(level_skill=level, then=order) for level, order in level_order.items()],
                output_field=IntegerField())).order_by('-level_ordering')
    except Exception as e:
        logger.warning(f'failed to connect to the database {e}')


def get_avatar_url(advertisement):
        return advertisement.user.userprofile.avatar.url


def get_user_language_skills(advertisement):
        LanguageSkill.objects.filter(user=advertisement.user)



def delete_ads(user, ads_id):
    ads = get_current_advertisement(ads_id)
    try:
        if ads.user == user:
            ads.delete()
            logger.info(f'delete ads {ads_id} user {user}')
        else:
            logger.warning(f'user {user} attempt to delete someone`s ads')
    except Exception as e:
        logger.error(f'error delete ads {ads_id} | {e}')

def choose_ads(user, ads_id):
    ads = get_current_advertisement(ads_id)
    try:
        add_new_notification(user, ads)
        room = f'{user}{ads.user.username}'
        return room
    except Exception as e:
        logger.error(f'failed to create dialogue room user {user} | {e}')
        return None

