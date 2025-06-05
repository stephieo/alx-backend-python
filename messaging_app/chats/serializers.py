from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
        exclude = [
            'groups', 'date_joined',
            'is_active', 'is_superuser', 'user_permissions'
        ]
# this  is a list of all the fields that should be (de)serialized( converted to/from JSON)
# these are fields that should only be serialized i.e they won't work with POST or PUT requests 


class ConversationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Conversation
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = '__all__'