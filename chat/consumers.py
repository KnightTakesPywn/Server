## Credit to: https://channels.readthedocs.io/en/latest/tutorial/index.html

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):

  ###################################
  ## Run When a Connection is Made ##
  ###################################

  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = 'chat_%s' % self.room_name

    # Save all messages that have been seen while in the room
    self.chatHistory = []
    self.username = {}
    self.users = []

    # Join room group
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )

    await self.accept()


  #################################
  ## Run When Connection is Lost ##
  #################################

  async def disconnect(self, close_code):
    # Leave room group
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )


  ####################################
  ## Revive Info From The Front End ##
  ####################################

  # Receive message from WebSocket
  async def receive(self, text_data):
    text_data_json = json.loads(text_data)

    if text_data_json['type'] == 'message':
      print('Received a message')
      await self.receive_message(text_data_json)

    elif text_data_json['type'] == 'newUser':
      await self.new_user(text_data_json)


  ###############################
  ## Different Receive Actions ##
  ###############################

  # User entered a new message
  async def receive_message(self, text_data):
    message = text_data['message']

    message =  self.username + ': ' + message
    # Send message to room group
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'chat_message',
        'message': message
      }
    )


  # New user connected to the server
  async def new_user(self, text_data):
    user = text_data['user']
    print(f'{user} Connected')
    self.username = user
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'add_user',
        'username': user
      }
    )


  ###################################
  ## Different Server Wide Actions ##
  ###################################

  # Receive message from room group
  async def chat_message(self, event):
    message = event['message']
    self.chatHistory.append(message)

    # Send message to WebSocket
    await self.send(text_data=json.dumps({
      'message': message,
      'history': self.chatHistory,
      'users': self.users
    }))


  async def add_user (self, event):
    username = event['username']
    self.users.append(username)
