from django.urls import path
from . import views

app_name = 'messaging'  # Optional: for namespacing URLs

urlpatterns = [
    
    path('user/delete/', views.delete_user, name='delete_user'), 
    path('conversation/<uuid:conversation_id>/messages/', views.display_conversation_msgs, name='display_conversation_messages'),
    path('message/<uuid:message_id>/history/', views.message_history_view, name='message_history'),
    path('messages/unread/', views.display_unread_messages_inbox, name='unread_messages_inbox'),
]