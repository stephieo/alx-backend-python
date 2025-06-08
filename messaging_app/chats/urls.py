from django.urls import path,include
from . import views
from rest_framework import routers 


router = routers.DefaultRouter()
router.register('conversations', views.ConversationViewset)
router.register('messages', views.MessageViewSet)
urlpatterns = [
    path('', include(router.urls))
    ]