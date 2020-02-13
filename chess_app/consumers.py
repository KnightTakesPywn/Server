from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .board import Board

class ChatConsumer(AsyncWebsocketConsumer):

  ###################################
  ## Run When a Connection is Made ##
  ###################################

  ## Runs when a user has connected to the game server
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = 'chess_%s' % self.room_name

    # Join room group
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )

    await self.accept()

    ## Create the game instance for this user
    await self.create_game()

    # Have all users update their game state. *Mainly for the
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'send_board'
      }
    )

  ##########################
  ## User Leaves the Room ##
  ##########################

  async def disconnect(self, close_code):
    # Leave room group
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )

  ####################
  ## Helper Methods ##
  ####################

  async def create_game(self):
    self.gameBoard = Board()
    print(self.gameBoard)



  #################################
  ## Message Receive From Client ##
  #################################

  # Receive message from WebSocket
  async def receive(self, text_data):
    data = json.loads(text_data)

    if data['type'] == 'create':
      await self.start_game()

    if data['type'] == 'move':
      await self.handle_move(data)

    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'send_board'
      }
    )

  ###############################
  ## Different Receive Actions ##
  ###############################

  async def handle_move(self, data):
    valid_move = self.gameBoard.move(data['start'],data['end'])
    if valid_move:
      await self.channel_layer.group_send(
        self.room_group_name,
        {
          "type": 'update_board',
          "board": self.gameBoard.objectify(),
        }
      )


  ####################################
  ## Different Server Message Sends ##
  ####################################

  # Receive message from room group
  async def send_board(self, event):
    turn = ("white","black")[self.gameBoard.player_to_move==-1]
    await self.send(text_data=json.dumps({
      'type':'gameState',
      'turn': turn,
      'board':self.gameBoard.objectify()
    }))

  ####################################
  ###  Group updates game board ######
  ####################################

  async def update_board(self,event):
    print("Call Event", event['board'])
    # self.gameBoard = event['board']
    self.send_board(event)
