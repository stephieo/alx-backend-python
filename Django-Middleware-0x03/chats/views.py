from django.shortcuts import render
from rest_framework import viewsets, filters, status
from .models import Conversation, Message, MessageStatus
from .serializers import ConversationSerializer, MessageSerializer
from .filters import MessageFilter
from .pagination import MessageResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .permissions import IsParticipantofConversation
from rest_framework.response import Response



# Create your views here.
#TODO: override create methods for both message and convo. Convo maker should automatically be participants
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all() #this is what is returned in a GET request 
    serializer_class = ConversationSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsParticipantofConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation_id', 'participants__user_id']

    def get_queryset(self):
        '''this override is one way of  enforcing access restriction'''
        user = self.request.user
        return Conversation.objects.filter(participants=user)
    
    def create(self, request, *args, **kwargs):
        '''ensuring the user creating a convo is made a participant'''
        data = request.data.copy() # cuz working with the original gives errors
        participants = data.get('participants', [])
        if str(request.user.user_id) not in [str(p) for p in participants]:
            participants.append(str(request.user.user_id))
        data['participants'] = participants
       
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
#TODO: OVerride get_queryset to restrict results to convo, and messages that user is part of
# [x] convo
# [ ] msgs

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_classes = [MessageResultsSetPagination]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['status', 'recipient']
    filterset_class = MessageFilter
    #TODO: we want to filter messages by converastion
    # we also want  the message  to be in order of creation date, newest first

    def get_queryset(self):
        '''this override is one way of  enforcing access restriction'''
        user = self.request.user
        return Message.objects.filter(sender=user)
    
    def create(self, request, *args, **kwargs):
        '''ensuring the user creating a message and the recipient are participants of the conversation
        note: a conversation must be created first before trying to send messages '''
        data = request.data.copy()
        recipient = data.get('recipient')
        conversation_id = data.get('conversation_id')
        participants = conversation_id.get('participants', [])
        if str(request.user.user_id) not in [str(p) for p in participants]:
            return Response({"error": "Sender must be a participant of the conversation"}, status=status.HTTP_403_FORBIDDEN)
        if str(recipient) not in [str(p) for p in participants]:
            return Response({"error": "Recipient must be a participant of the conversation"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
