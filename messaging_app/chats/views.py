from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Conversation, Message, MessageStatus
from .serializers import ConversationSerializer, MessageSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# Create your views here.

class ConversationViewset(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation_id']
    

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['status', 'recipient']
    filterset_fields = ['status', 'conversation_id']
    #TODO: we want to filter messages by converastion
    # we also want  the messaged  to be in order ofcreation dat, newst first