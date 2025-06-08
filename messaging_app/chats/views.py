from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Conversation, Message, MessageStatus
from .serializers import ConversationSerializer, MessageSerializer
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation_id', 'participants__user_id']
    
#TODO: OVerride get_queryset in both to restrict results to covo, and messages that user is paer of
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['status', 'recipient']
    filterset_class = MessageFilter
    #TODO: we want to filter messages by converastion
    # we also want  the messaged  to be in order ofcreation dat, newst first