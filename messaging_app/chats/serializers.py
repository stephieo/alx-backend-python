from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True, source='get_full_name')
    class Meta:
        model = User
        fields = ['user_id', 'email',  'phone_number' 'last_name']
# this  is a list of all the fields that should be (de)serialized( converted to/from JSON)
# these are fields that should only be serialized i.e they won't work with POST or PUT requests 


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['message_id', 'sender', 'conversation']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True) 
    # the many  means that yo're expecting more tha one message to be returned
    # the read-only means that messages are ntot required to create a conversation 

    class Meta:
        model = Conversation
        fields = '__all__'
        exclude =['conversation_id']

