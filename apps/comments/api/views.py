from rest_condition import Or, And
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.permissions import RequestIsUpdate, RequestIsDelete, UserIsStaff, RequestIsReadOnly
from apps.comments.api.permissions import UserIsCommentAuthor
from apps.comments.api.retrievers import CommentRetriever
from apps.comments.api.serializers import CommentSerializer, CommentBannedSerializer
from apps.posts.api.retrievers import PostRetriever


class PostCommentListCreate(generics.ListCreateAPIView, PostRetriever):

    permission_classes = (
        IsAuthenticated,
    )

    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.post_instance.comment_set.prefetch_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.post_instance)


class CommentDetails(generics.RetrieveUpdateDestroyAPIView, CommentRetriever):

    permission_classes = (
        IsAuthenticated,
        Or(
            RequestIsReadOnly,
            And(
                RequestIsUpdate,
                UserIsCommentAuthor,
            ),
            And(
                RequestIsDelete,
                Or(UserIsCommentAuthor, UserIsStaff)
            )
        )
    )

    serializer_class = CommentSerializer

    def get_object(self):
        return self.comment_instance


class CommentBannedDetails(generics.RetrieveUpdateAPIView, CommentRetriever):

    permission_classes = (
        IsAuthenticated,
        UserIsStaff
    )

    serializer_class = CommentBannedSerializer

    def get_object(self):
        return self.comment_instance

    def perform_update(self, serializer):
        serializer.save(banned_by_id=self.request.user.id)
