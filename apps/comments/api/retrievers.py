from django.shortcuts import get_object_or_404
from rest_framework import generics

from apps.comments.models import Comment


class CommentRetriever(generics.GenericAPIView):

    _comment = None

    @property
    def comment_instance(self):
        assert 'comment_id' in self.kwargs
        if not self._comment:
            self._comment = get_object_or_404(
                Comment.objects.prefetch_related(
                    'author',
                    'post',
                    'post__author'
                ),
                id=self.kwargs.get('comment_id')
            )
        return self._comment
