# Built in imports.
import json  # Third Party imports.
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer  # Django imports.
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser  # Local imports.


# File "/Users/adam/Documents/tmobile/coding/estimate/app/consumer.py", line 18, in connect
#   if self.scope['user'] == AnonymousUser():
# KeyError: 'user'
# WebSocket DISCONNECT /ws/live-score/1 [127.0.0.1:54868]

class LiveScoreConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_name = "channel_test"
        self.group_name = "group_test"

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['game_id']
        self.room_name = "room_1"
        self.room_group_name = "group_1"
        await self.channel_layer.group_add(
            "group_test",
            "channel_test"
        )  # If invalid game id then deny the connection.
        try:
            # self.game = Game.objects.get(pk=self.room_name)
            self.game = "game obj"
        except ObjectDoesNotExist:
            raise DenyConnection("Invalid Game Id")
            await self.accept()

    async def receive(self, text_data):
        game_city = "game_city"
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'live_score',
                'game_id': self.room_name,
                'game_city': game_city
            }
        )

    async def live_score(self, event):
        await self.send(text_data=json.dumps({
            'score': 23,
        }))

    async def websocket_disconnect(self, message):
        print(self.channel_name)
        print("message: ", message)
        await self.channel_layer.group_discard(
            "group_test",
            "channel_test"
        )
