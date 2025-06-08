from rest_framework import permissions 

class IsParticipantofConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return object.participants.filter(id=request.user.id).exists()
        return False
