from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('conversations', views.ConversationViewset)
urlpatterns = [
    path('conversations/', include(router.urls))
]