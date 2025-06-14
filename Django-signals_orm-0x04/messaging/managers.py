from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user_instance):
        """
        Retrieves messages that are marked as unread for the given user,
        where the user is the receiver.
        Optimized to fetch only necessary fields.
        """
        return self.get_queryset().filter(
            receiver=user_instance,
            unread=True  # Assuming 'unread' is a BooleanField on your Message model
        ).select_related('sender').only(
            'message_id',       # From Message model
            'content',          # From Message model
            'timestamp',        # From Message model
            'sender__username'  # From related User model (sender's username)
        ).order_by('-timestamp') # Optional: show newest unread messages first