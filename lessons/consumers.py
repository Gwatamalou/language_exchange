import json
from redis.asyncio import Redis
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        self.redis = Redis()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.redis.close()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json.get('username', 'unknown')

        # Отправка сообщения в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': username,
                'message': message,
                'sdp': text_data_json.get('sdp'),
                'ice': text_data_json.get('ice')
            }
        )


    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        sdp = event.get('sdp')
        ice = event.get('ice')

        await self.send(text_data=json.dumps({
            'username': username,
            'message': message,
            'sdp': sdp,
            'ice': ice
        }))
