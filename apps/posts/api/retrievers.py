from django.shortcuts import get_object_or_404
from rest_framework import generics

from apps.posts.models import Post


class PostRetriever(generics.GenericAPIView):

    _post = None

    @property
    def post_instance(self):
        assert 'post_id' in self.kwargs
        if not self._post:
            self._post = get_object_or_404(
                Post.objects.prefetch_related(
                    'author',
                    'comment_set',
                    'comment_set__author'
                ),
                id=self.kwargs.get('post_id')
            )
        return self._post
