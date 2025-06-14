""" This file is basically used to  define reciever functions
 for the different builtin model, request or authentication signals"""

from .models import Message, Notification, User, MessageHistory
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db.models  import Q


@receiver(post_save, sender=Message) # this decorator takes the same kwargs as Signal.connect()
def send_message_notification(sender, instance, created, **kwargs): # the arguments of a reciever depend on what the signal sends
    """ so this function is a reciever that listens
      for a post_save signal from the Message model 
      and then creates a notification for that message"""
    if created:
         Notification.objects.create(
              user=instance.receiver,
              message=f"new message from {instance.sender.username}: {instance.content[:20]}"
         )
         print(f"Notification created for {instance.receiver.username} for message {instance.message_id}")


@receiver(pre_save, sender=Message)
def save_message_history(sender, instance, **kwargs):
    try:
        saved_msg = Message.objects.get(pk=instance.pk)
        if saved_msg and instance.content != saved_msg.content:
            MessageHistory.objects.create(
                edited_by=instance.sender,
                message=instance,
                old_message_version= saved_msg.content,
            )
            instance.is_edited = True
            instance.edited_at = timezone.now()
    except Message.DoesNotExist:
        pass


@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    #retrieve and delete all messages
    user_messages = Message.objects.filter(
        Q(sender=instance)/
        Q(receiver=instance)
        ).delete()
    # and notifs
    user_notifs = Notification.objects.filter(user_id=instance).delete()
    # and msg history
    user_msg_history = MessageHistory.objects.filter(edited_by=instance).delete()
