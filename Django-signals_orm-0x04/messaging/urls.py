from django.urls import path
from . import views

app_name = 'messaging'  # Optional: for namespacing URLs

urlpatterns = [
    # ... other urls for your messaging app ...
    path('user/delete/', views.delete_user, name='delete_user'), # Assuming you want a URL for this too
    path('conversation/<uuid:conversation_id>/messages/', views.display_conversation_msgs, name='display_conversation_messages'),
]