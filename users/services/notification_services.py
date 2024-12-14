from django.db import transaction


import logging

logger = logging.getLogger(__name__)

from advertisements.models import Notification

__all__ = [
    'notification_accept',
    'notification_delete',
    'get_current_notification',
    'get_notification',
]


def get_notification(user_id):
    try:
        return Notification.objects.filter(user_id=user_id)
    except Exception as e:
        logger.warning(f'failed to connect to the database {e}')
        return None


def get_current_notification(notification_id, user):
    try:
        return Notification.objects.get(id=notification_id, user=user)
    except Notification.DoesNotExist:
        return None


@transaction.atomic
def notification_accept(notification):
    try:
        room = notification.room
        notification.delete()
        logger.info(f'notification {notification} accept')
        return room
    except Exception as e:
        logger.error(f'failed accept notification {notification} | {e}')
        return False


@transaction.atomic
def notification_delete(notification):
    try:
        notification.delete()
        logger.info(f'notification {notification} decline')
    except Exception as e:
        logger.error(f'failed decline notification {notification} | {e}')


