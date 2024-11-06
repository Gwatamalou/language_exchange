from django.shortcuts import get_object_or_404
from advertisements.models import Advertisement, Notification


__all__ = [
    'get_current_advertisement',
    'add_new_advertisement',
    'add_new_notification'
]


def get_current_advertisement(slug_id):
    """Возвращает выбранное объявление"""
    return get_object_or_404(Advertisement, id=slug_id)


def add_new_advertisement(user, form):
    """Добавляет новое объявление в БД"""
    if form.is_valid():
        advertisement = form.save(commit=False)
        if not Advertisement.objects.filter(user=user, language_to_learn=advertisement.language_to_learn,
                                            language_level_to_learn=advertisement.language_level_to_learn).exists():
            advertisement.user = user
            advertisement.save()


def add_new_notification(user, ads):
    """Создает уведомление по выбранному объявлению"""
    if not Notification.objects.filter(responder=user, user=ads.user, advertisement=ads).exists():
        Notification.objects.create(
            responder=user,
            user=ads.user,
            advertisement=ads,
            room=f'{user}{ads.user.username}',
        )
