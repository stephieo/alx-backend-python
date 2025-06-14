from django.test import TestCase
from .models import Message, Notification, User
from django.db.models.signals import post_save
from django.dispatch import receiver

class MessageSignalTests(TestCase):
    """Test cases for the Message signals functionality"""
    
    def setUp(self):
        """Create test users for our test cases"""
        # Create sender user
        self.sender = User.objects.create_user(
            username='testsender',
            email='sender@example.com',
            password='password123'
        )
        
        # Create receiver user
        self.receiver = User.objects.create_user(
            username='testreceiver',
            email='receiver@example.com',
            password='password123'
        )
        
        # Initial notification count
        self.initial_notification_count = Notification.objects.count()
    
    def test_notification_created_when_message_saved(self):
        """Test that a notification is created when a message is saved"""
        # Create a new message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="This is a test message"
        )
        
        # Check that a notification was created
        self.assertEqual(
            Notification.objects.count(), 
            self.initial_notification_count + 1,
            "A notification should be created when a message is saved"
        )
        
        # Get the notification
        notification = Notification.objects.latest('id')
        
        # Check notification properties
        self.assertEqual(notification.user, self.receiver)
        self.assertIn(self.sender.username, notification.message)
        self.assertIn(message.content[:20], notification.message)
    
    def test_notification_not_created_when_message_updated(self):
        """Test that a notification is not created when a message is updated"""
        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original message"
        )
        
        # Get the notification count after creating the message
        notification_count_after_create = Notification.objects.count()
        
        # Update the message
        message.content = "Updated message"
        message.save()
        
        # Check that no new notification was created
        self.assertEqual(
            Notification.objects.count(), 
            notification_count_after_create,
            "No new notification should be created when a message is updated"
        )
    
    def test_signal_with_multiple_messages(self):
        """Test signal behavior with multiple messages"""
        # Create several messages
        for i in range(3):
            Message.objects.create(
                sender=self.sender,
                receiver=self.receiver,
                content=f"Test message {i}"
            )
        
        # Check that the correct number of notifications was created
        self.assertEqual(
            Notification.objects.count(), 
            self.initial_notification_count + 3,
            "Three notifications should be created for three messages"
        )

