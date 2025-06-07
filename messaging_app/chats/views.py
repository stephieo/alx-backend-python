from django.shortcuts import render
from rest_framework import viewsets
from .models import Conversation, Message, MessageStatus
from .serializers import ConversationSerializer, MessageSerializer
# from rest_framework.permissions import AllowAny
# Create your views here.

class ConversationViewset(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    # permission_classes = [AllowAny]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes = [AllowAny]
