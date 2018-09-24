from rest_framework import permissions


class BaseNoObjectPermission(permissions.BasePermission):
    """ Base class for all permission classes, where permissions are determined
        by view kwargs (such as 'model_id').

        This class should be used to have consistent behavior for cases when permissions check
        is performed by explicit call of self.check_object_permission() method in a view.
    """

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class UserIsStaff(BaseNoObjectPermission):

    def has_permission(self, request, view):
        return request.user.is_staff


class UserIsSuperuser(BaseNoObjectPermission):

    def has_permission(self, request, view):
        return request.user.is_superuser


class RequestIsReadOnly(BaseNoObjectPermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class RequestIsCreate(BaseNoObjectPermission):

    def has_permission(self, request, view):
        return request.method == 'POST'


class RequestIsUpdate(BaseNoObjectPermission):

    def has_permission(self, request, view):
        return request.method in ['PUT', 'PATCH']


class RequestIsDelete(BaseNoObjectPermission):

    def has_permission(self, request, view):
        return request.method == 'DELETE'
