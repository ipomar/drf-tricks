from api.permissions import BaseNoObjectPermission


class UserIsPostAuthor(BaseNoObjectPermission):

    def has_permission(self, request, view):
        assert hasattr(view, 'post_instance')
        return view.post_instance.author == request.user
