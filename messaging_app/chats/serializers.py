from rest_framework import serializers
from .models import User, Message, Conversation, MessageStatus

class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True, source='get_full_name')
    class Meta:
        model = User
        fields = ['user_id', 'email',  'phone_number', 'display_name']
# this  is a list of all the fields that should be (de)serialized( converted to/from JSON)
        read_only_fields = ['user_id']
# these are fields that should only be serialized i.e they won't work with POST or PUT requests 


class MessageSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['message_id', 'sender', 'conversation']

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("message cannot be empty")
    
    def validate_status(self,value):
        if value not in [choice[0] for choice in MessageStatus]:
            raise serializers.ValidationError("invalid message status")


class ConversationSerializer(serializers.ModelSerializer):
    conversation_title = serializers.SerializerMethodField()
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True) 
    # the many  means that yo're expecting more tha one message to be returned
    # the read-only means that messages are ntot required to create a conversation 

    class Meta:
        model = Conversation
        exclude =['conversation_id']
    # TODO: change logiv to include name for >2 participants
    def get_conversation_title(self,obj):
        participants = obj.participants.all()
        return f"{participants[0].get_short_name()} and {participants[1].get_short_name()}"
    
    def validate_participants(self, value):
        if length(value) < 2:
            raise serializers.ValidationError("conversation must have at least 2 participants")
    
    
