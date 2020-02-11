## Credit to: https://channels.readthedocs.io/en/latest/tutorial/index.html

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = 'chat_%s' % self.room_name

    # Save all messages that have been seen while in the room
    self.chatHistory = []

    # Join room group
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )

    await self.accept()

  async def disconnect(self, close_code):
    # Leave room group
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )

  # Receive message from WebSocket
  async def receive(self, text_data):
    text_data_json = json.loads(text_data)
    message = text_data_json['message']
    user = text_data_json['user']

    message =  user + ': ' + message
    # Send message to room group
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'chat_message',
        'message': message
      }
    )

  # Receive message from room group
  async def chat_message(self, event):
    message = event['message']
    self.chatHistory.append(message)

    # Send message to WebSocket
    await self.send(text_data=json.dumps({
      'message': message,
      'history': self.chatHistory
    }))
