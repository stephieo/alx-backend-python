from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Conversation, Message, MessageStatus
from .serializers import ConversationSerializer, MessageSerializer
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .permissions import IsConversationParticipant
# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all() #this is what is returned in a GET request 
    serializer_class = ConversationSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation_id', 'participants__user_id']

    def get_queryset(self):
        '''this override is one way of  enforcing access restriction'''
        user = self.request.user
        return Conversation.objects.filter(participants=user)
    
#TODO: OVerride get_queryset to restrict results to convo, and messages that user is part of
# [x] convo
# [x] msgs

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['status', 'recipient']
    filterset_class = MessageFilter
    #TODO: we want to filter messages by converastion
    # we also want  the message  to be in order ofcreation dat, newst first

    def get_queryset(self):
        '''this override is one way of  enforcing access restriction'''
        user = self.request.user
        return Message.objects.filter(sender=user)