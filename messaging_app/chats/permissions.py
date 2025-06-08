from rest_framework import permissions 

class IsParticipantofConversation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return object.participants.filter(id=request.user.id).exists()
