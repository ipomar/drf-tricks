from rest_condition import Or, And
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.permissions import RequestIsReadOnly, RequestIsUpdate, UserIsSuperuser, RequestIsDelete
from apps.posts.api.permissions import UserIsPostAuthor
from apps.posts.api.retrievers import PostRetriever
from apps.posts.api.serializers import PostContentSerializer
from apps.posts.models import Post


class PostListCreate(generics.ListCreateAPIView):

    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = PostContentSerializer
    queryset = Post.objects.prefetch_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
        return self.post_instance
