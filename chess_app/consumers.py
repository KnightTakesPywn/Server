from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .game_logic.board import Board

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = 'chat_%s' % self.room_name

    # Join room group
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )

    await self.accept()

    self.board = {}


  async def start_game(self):
    json_data = open('SampleData/startingBoard.json')
    data = json.load(json_data)
    self.board = data['data']


  async def disconnect(self, close_code):
    # Leave room group
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )


  # Receive message from WebSocket
  async def receive(self, text_data):
    text_data_json = json.loads(text_data)

    await self.start_game()
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'send_board'
      }
    )


  # Receive message from room group
  async def send_board(self, event):
    await self.send(text_data=json.dumps({
      'gameState': {
        'turn':'white',
        'board':self.board
        },
    }))
