from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Message, Notification, MessageHistory
#INCOMPLETE :I've only focused on signal implementation here. Need to import previous stuff done from either middleware or messagingapp projects.

# Create your views here.
@api_view(['DELETE'])
def delete_user(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    return Response("User Deleted")