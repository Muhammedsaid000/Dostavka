from rest_framework import permissions


class CheckUserCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role=='Owner':
            return True
        elif request.user.user_role == 'Administrator':
            return True
        return False



class CheckReviewCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role=='Owner':
            return False
        return True


class CheckOrderCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role=='Owner':
            return False
        elif request.user.user_role=='Courier':
            return False
        return True


class CheckCourierReview(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role=='Courier':
            return True
        elif request.user.user_role=='Administrator':
            return True
        return False


class CheckReviewEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user==obj.client
        return False