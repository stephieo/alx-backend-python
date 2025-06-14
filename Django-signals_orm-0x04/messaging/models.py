from django.db import models
from django.contrib.auth.models import User
import uuid
from .managers import UnreadMessagesManager
# TODO:I've only focused on signal implementation here. Need to import previous stuff done from either middleware or messagingapp projects.

# Create your models here.
# Not defining a custom user model  for this, using the default Django user.
# Django's built-in User model fields:
# username, first_name, last_name, email, password, groups, user_permissions,
# is_staff, is_active, is_superuser, last_login, date_joined

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, db_table='conversation_participants')

class Message(models.Model):

    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE,
                                        null=True, blank=True, related_name='replies')
    edited_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_sent = models.BooleanField(default=True)
    is_delivered = models.BooleanField(default=False)
    unread = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)

    objects = models.Manager()  
    unread_messages = UnreadMessagesManager()  # Custom manager for unread messages
    
    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username} - {self.content[:20]}...'

class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username} - {self.message.content[:20]}...'

class MessageHistory(models.Model):
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_history')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_message_version = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    


