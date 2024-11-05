from django.db import transaction

from advertisements.models import Notification

__all__ = [
    'notification_accept',
    'notification_delete',
    'get_current_notification',
    'get_notification',
]


def get_notification(user_id):
    return Notification.objects.filter(user_id=user_id)


def get_current_notification(notification_id, user):
    try:
        Notification.objects.get(id=notification_id, user=user)
    except Notification.DoesNotExist:
        return None


@transaction.atomic
def notification_accept(notification):
    room = notification.room
    notification.delete()
    return room


@transaction.atomic
def notification_delete(notification):
    notification.delete()
