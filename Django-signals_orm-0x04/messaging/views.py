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
    messages = Message.objects.filter(
        sender=request.user,
        conversation_id=conversation_id).order_by('timestamp')
    
    if not messages:
        return Response({"error": "No messages found for this conversation."}, status=404)
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



@api_view(['GET'])
def display_message_thread(request, message_id):
    '''displaying a single message thread'''
    message = Message.objects.filter(id=message_id).prefetch_related('replies')
    if not message.exists():
        return Response({"error": "Message not found."}, status=404)
    data = {
        "id": message[0].id,
        "sender": message[0].sender.id,
        "content": message[0].content,
        "timestamp": message[0].timestamp,
        "replies": [
            {
                "id": reply.id,
                "sender": reply.sender.id,
                "content": reply.content,
                "timestamp": reply.timestamp
            } for reply in message[0].replies.all()
        ]
    }
    return Response(data)


