from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from .models import User, Message, Notification, MessageHistory
#INCOMPLETE :I've only focused on signal implementation here. Need to import previous stuff done from either middleware or messagingapp projects.

# Create your views here.
@api_view(['DELETE'])
def delete_user(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    return Response("User Deleted")

@cache_page(60)
@api_view(['GET'])
def display_conversation_msgs(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
    data = [
        {
            "id": msg.id,
            "sender": msg.sender.id,
            "content": msg.content,
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]
    return Response(data)