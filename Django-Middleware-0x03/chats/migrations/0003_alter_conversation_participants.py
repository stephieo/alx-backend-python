# Generated by Django 5.2.1 on 2025-06-08 20:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='participants',
            field=models.ManyToManyField(db_table='conversation_participants', to=settings.AUTH_USER_MODEL),
        ),
    ]
