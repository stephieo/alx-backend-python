""" This file is basically used to  define reciever functions
 for the different builtin model, request or authentication signals"""

from .models import Message, Notification, User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Message) # this decorator ale the same kwargs as Signal.connect()
def send_message_notification(sender, instance, created, **kwargs): # the arguments of a reciever depend on what the signal sends
    """ so this function is a reciever that listens
      for a post_save signal from the Message model 
      and then creates a notification for that message"""
    if created:
         Notification.objects.create(
              user=instance.receiver,
              message=f"new message from {instance.sender.username}: {instance.content[:20]}"
         )
         print(f"Notification created for {instance.reciever.username} for message {instance.message_id}")