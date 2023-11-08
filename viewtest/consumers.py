import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class RequestConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_slug"]
        self.room_group_name = "group_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        print("connecting to: ", self.room_group_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_wrapped = json.loads(text_data)
        context = text_wrapped
        print('message received, trying to send to: ', self.room_group_name)
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': 'request_data_message',
                                                                            'message': context})
        self.send(text_data=json.dumps(context))

    def request_data_message(self, event):
        message = {}
        if 'message' in event:
            if isinstance(event['message'], dict):
                message = event['message']
            else:
                message['message'] = event['message']
        self.send(text_data=json.dumps(message))
