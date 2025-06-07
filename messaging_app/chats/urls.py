from django.urls import path
from . import views
from rest_framework import routers 


router = routers.DefaultRouter()
router.register('conversations', views.ConversationViewset)
urlpatterns =router.urls