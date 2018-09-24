from django.shortcuts import get_object_or_404
from rest_framework import generics

from apps.comments.models import Comment


class CommentRetriever(generics.GenericAPIView):

    _comment = None

    @property
    def comment(self):
        assert 'comment_id' in self.kwargs
        if not self._comment:
            self._comment = get_object_or_404(Comment, id=self.kwargs.get('comment_id'))
        return self._comment
