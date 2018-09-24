from rest_condition import Or, And
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.permissions import RequestIsReadOnly, RequestIsUpdate, UserIsSuperuser, UserIsStaff, RequestIsDelete
from apps.posts.api.permissions import UserIsPostAuthor
from apps.posts.api.retrievers import PostRetriever
from apps.posts.api.serializers import PostContentSerializer, PostBanSerializer
from apps.posts.models import Post


class PostListCreate(generics.ListCreateAPIView):

    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = PostContentSerializer
    queryset = Post.objects.all()


class PostDetails(generics.RetrieveUpdateDestroyAPIView, PostRetriever):

    permission_classes = (
        IsAuthenticated,
        Or(
            RequestIsReadOnly,
            And(
               RequestIsUpdate,
               UserIsPostAuthor
            ),
            And(
                RequestIsDelete,
                Or(UserIsPostAuthor, UserIsSuperuser)
            )
        )
    )

    serializer_class = PostContentSerializer

    def get_object(self):
        return self.post


class PostBanDetails(generics.UpdateAPIView, PostRetriever):

    permission_classes = (
        IsAuthenticated,
        Or(UserIsStaff, UserIsSuperuser)
    )

    serializer_class = PostBanSerializer

    def get_object(self):
        return self.post
