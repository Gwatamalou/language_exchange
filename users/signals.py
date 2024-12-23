from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from advertisements.models import Notification


@receiver(post_save, sender=Notification)
def notify_user(sender, instance, created, **kwargs):
    """
    отслеживает запись в таблицу уведомлений
    отправляет сообщения по websoсket для формирования push notify
    """
    if created:
            user_id = instance.user_id
            notify_id = instance.id
            channel_layer = get_channel_layer()
            group_name = f'user_{user_id}'
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'send_notification',
                    'message': 'Notification.user.user_id',
                    'notify_id': notify_id,
                }
            )
