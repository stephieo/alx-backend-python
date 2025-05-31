from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    USER_TYPES = [
        ('guest','Guest'),
        ('host', 'Host'),
        ('Admin','admin')
    ]
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=250) 
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    password_hash = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250, null=True)
    role = models.CharField(max_length=100, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    