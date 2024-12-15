from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

import json

from users.services import notification_services as ntfy



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.group_name = f'user_{self.user.id}'

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()


    async def disconnect(self, code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        async def receive(self, text_data=None, bytes_data=None):
            data = json.loads(text_data)
            action = data.get('action')
            notify_id = data.get('notify_id')

            if action == 'accept':
                room = await sync_to_async(ntfy.notification_accept)(notify_id)
                if room:
                    await self.send(text_data=json.dumps({
                        'status': 'success',
                        'redirect_url': f'/lesson/{room.id}/'
                    }))

            elif action == 'decline':
                await sync_to_async(ntfy.notification_delete)(notify_id)
                await self.send(text_data=json.dumps({
                    'status': 'success',
                    'message': 'Notification declined'
                }))

    async def send_notification(self, event):
        message = event['message']
        notify_id = event['notify_id']
        await self.send(text_data=json.dumps({
            'message': message,
            'notify_id': notify_id,
        }))

