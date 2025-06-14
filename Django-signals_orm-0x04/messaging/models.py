from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
# Not defining a custom user model  for this, using the default Django user.
# Django's built-in User model fields:
# username, first_name, last_name, email, password, groups, user_permissions,
# is_staff, is_active, is_superuser, last_login, date_joined


class Message(models.Model):

    class Status(models.TextChoices):
        SENT = 'sent', 'Sent'
        DELIVERED = 'delivered', 'Delivered'
        READ = 'read', 'Read'

    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SENT
    )
    
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
