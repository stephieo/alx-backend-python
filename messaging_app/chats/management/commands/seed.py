from django.core.management.base import BaseCommand
from django.conf import settings
import os
import json
import uuid
from datetime import datetime
from django.utils import timezone
from chats.models import User, Conversation, Message, MessageStatus

#TODO:
#[ ]: fix all errors in running this command
# [ ]: seed database successfully 
class Command(BaseCommand):
    help = "Initializes the app database with test data from a JSON file."

    def add_arguments(self, parser):
        """Defines optional and required arguments for the command."""
        parser.add_argument('filename', default='app_data.json', type=str)

    def handle(self, *args, **options):
        filename = options['filename']
        file_path = os.path.join(settings.BASE_DIR, filename)

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.seed_users(data.get('users', []))
                self.seed_conversations(data.get('conversations', []))
                self.seed_messages(data.get('messages', []))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON format"))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))

    def seed_users(self, users):
        """Seeds User model data from JSON."""
        for user_data in users:
            try:
                user_id = uuid.UUID(user_data.get('user_id'))
                email = user_data.get('email')
                if User.objects.filter(user_id=user_id).exists() or User.objects.filter(email=email).exists():
                    self.stdout.write(self.style.ERROR(f"User {email} already exists, skipping..."))
                    continue

                User.objects.create(
                    user_id=user_id,
                    email=email,
                    first_name=user_data.get('first_name'),
                    last_name=user_data.get('last_name'),
                    password=user_data.get('password'),  # Assuming raw password; use set_password for production
                    phone_number=user_data.get('phone_number', None),
                    created_at=user_data.get('created_at', timezone.now())
                )
            except ValueError:
                self.stdout.write(self.style.ERROR(f"Invalid user_id for {email}, skipping..."))

    def seed_conversations(self, conversations):
        """Seeds Conversation model data from JSON."""
        for conv_data in conversations:
            try:
                conversation_id = uuid.UUID(conv_data.get('conversation_id'))
                if Conversation.objects.filter(conversation_id=conversation_id).exists():
                    self.stdout.write(self.style.ERROR(f"Conversation {conversation_id} already exists, skipping..."))
                    continue

                participant_ids = conv_data.get('participants', [])
                participants = []
                for pid in participant_ids:
                    try:
                        participant_id = uuid.UUID(pid)
                        participant = User.objects.filter(user_id=participant_id).first()
                        if not participant:
                            self.stdout.write(self.style.ERROR(f"Participant {pid} not found for conversation {conversation_id}, skipping..."))
                            continue
                        participants.append(participant)
                    except ValueError:
                        self.stdout.write(self.style.ERROR(f"Invalid participant UUID {pid} for conversation {conversation_id}, skipping..."))
                        continue

                if not participants:
                    self.stdout.write(self.style.ERROR(f"No valid participants for conversation {conversation_id}, skipping..."))
                    continue

                conversation = Conversation.objects.create(
                    conversation_id=conversation_id,
                    created_at=conv_data.get('created_at', timezone.now())
                )
                conversation.participants.set(participants)
                conversation.save()
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f"Invalid conversation_id {conv_data.get('conversation_id')}, skipping..."))

    def seed_messages(self, messages):
        """Seeds Message model data from JSON."""
        for msg_data in messages:
            try:
                message_id = uuid.UUID(msg_data.get('message_id'))
                if Message.objects.filter(message_id=message_id).exists():
                    self.stdout.write(self.style.ERROR(f"Message {message_id} already exists, skipping..."))
                    continue

                conversation_id = uuid.UUID(msg_data.get('conversation_id'))
                sender_id = uuid.UUID(msg_data.get('sender_id'))
                recipient_id = uuid.UUID(msg_data.get('recipient_id'))
                
                conversation = Conversation.objects.filter(conversation_id=conversation_id).first()
                sender = User.objects.filter(user_id=sender_id).first()
                recipient = User.objects.filter(user_id=recipient_id).first()
                
                if not (conversation and sender and recipient):
                    self.stdout.write(self.style.ERROR(f"Invalid conversation, sender, or recipient for message {message_id}, skipping..."))
                    continue

                status = msg_data.get('status')
                if status not in [choice[0] for choice in MessageStatus.choices]:
                    self.stdout.write(self.style.ERROR(f"Invalid status for message {message_id}, skipping..."))
                    continue

                Message.objects.create(
                    message_id=message_id,
                    conversation=conversation,
                    sender=sender,
                    recipient=recipient,
                    message_body=msg_data.get('message_body'),
                    sent_at=msg_data.get('sent_at', timezone.now()),
                    status=status
                )
            except ValueError as e:
                raw_id = msg_data.get('message_id', 'unknown')
                self.stdout.write(self.style.ERROR(f"Invalid UUID for message {raw_id}: {str(e)}, skipping..."))