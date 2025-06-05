from django.db import models
from django.contrib.auth.models import AbstractUser 
import uuid
#TODO: i'd need to ccome back again to implement andy needed methods
# Create your models here.


class User(AbstractUser):

    USERNAME_FIELD = 'email' # this is a unique identifier tha can be used for AUTHENTICATION (login); 
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']
    
    username = None #NOTE: i can set this to first + lastname with save() later
    
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #The primary_key is for DATABASE use 
    email = models.EmailField(max_length=250, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=250) 
    last_name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    
    #TODO: add inexing to user_id, and email
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [models.Index(fields=['user_id', 'email'])]

class MessageStatus():
    SENT = 'sent'
    DELIVERED = 'delivered'
    READ ='read'

class Message(models.Model):

    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=150,
        choices=[status.value, status.name.capitalize() for  status in MessageStatus]
    )


    class Meta:
        indexes = [models.Index(fields=['sender_id', 'recipient_id', 'sent_at'])]
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, db_table='conversation_particpants')

