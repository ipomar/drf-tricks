from api.permissions import BaseNoObjectPermission


class UserIsCommentAuthor(BaseNoObjectPermission):

    def has_permission(self, request, view):
        return view.comment_instance.author == request.user


class UserIsCommentPostAuthor(BaseNoObjectPermission):

    def has_permission(self, request, view):
        return view.comment_instance.post.author == request.user
