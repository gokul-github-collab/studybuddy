from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms:id'
    ]
    return Response(routes)

@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serialized_data = RoomSerializer(rooms, many=True)
    return Response(serialized_data.data)


@api_view(['GET'])
def get_room(request, pk):
    room = Room.objects.get(id=pk)
    serialized_data = RoomSerializer(room)
    return Response(serialized_data.data)