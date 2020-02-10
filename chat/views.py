## Credit to: https://channels.readthedocs.io/en/latest/tutorial/index.html
from django.shortcuts import render

def index(request):
  return render(request, 'index.html', {})

def room(request, room_name):
  return render(request, 'room.html', {
    'room_name': room_name
  })
