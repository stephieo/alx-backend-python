import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = {
            'status': ['exact'],
            'sender__user_id': ['iexact', 'icontains'],
            'recipient__user_id': ['iexact', 'icontains'],
            'conversation_id': ['exact']

        }