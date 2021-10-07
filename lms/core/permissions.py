from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self,request,view):

        # if method is GET return True
        if request.method in SAFE_METHODS:
            return True

        # if user is Admin return True
        if request.user.is_staff:
            return True
            
        # else return False
        return False