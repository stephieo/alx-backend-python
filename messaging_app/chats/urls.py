from django.urls import path,include
from . import views
from rest_framework import routers 
from rest_framework_nested.routers import NestedDefaultRouter


router = routers.DefaultRouter()
router.register('conversations', views.ConversationViewSet)
router.register('messages', views.MessageViewSet)

nested_messages_router = NestedDefaultRouter(router, r'conversations', lookup='conversations')
nested_messages_router.register(r'books', views.MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_messages_router.urls)),
    ]