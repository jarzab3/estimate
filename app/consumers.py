import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from app.models import SessionEntry, EstimateSession
from channels.layers import get_channel_layer


def get_users(estimate_session):
    session_entries = SessionEntry.objects.filter(estimate_session=estimate_session)
    users = [{
        'id': entry.id,
        'user_name': entry.user_name,
    } for entry in session_entries]
    return users


def get_user(estimate_session, channel):
    session_entry = SessionEntry.objects.get(estimate_session=estimate_session, channel=channel)
    user = [{'channel': session_entry.channel,
             'user_name': session_entry.user_name}]
    return user


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.estimate_session = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        self.estimate_session = EstimateSession.objects.filter(code=int(self.room_name)).first()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        session_users = get_users(self.estimate_session)

        # Update users list
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(self.channel_name, {
            "type": "chat.message",
            'message': {"type": "add", "content": session_users}
        })

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("Disconnecting: ", self.channel_name)

        # Remove entry from db
        se = SessionEntry.objects.get(channel=self.channel_name)

        # Update all users about disconnected users
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {"type": "delete", "id": se.id}
            }
        )

        se.delete()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        se = SessionEntry.objects.create(estimate_session=self.estimate_session, user_name=str(message),
                                         channel=self.channel_name)
        se.save()

        if type(message) == str:
            message = [{"id": se.id, "user_name": message}]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {"type": "add", "content": message}
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
