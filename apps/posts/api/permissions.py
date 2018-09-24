from api.permissions import BaseNoObjectPermission


class UserIsPostAuthor(BaseNoObjectPermission):

    def has_permission(self, request, view):
        assert hasattr(view, 'post')
        return view.post.author == request.user
