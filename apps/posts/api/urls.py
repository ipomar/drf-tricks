from django.conf.urls import url

from apps.comments.api.views import PostCommentListCreate
from apps.posts.api.views import PostListCreate, PostDetails

# /api/post/...

urlpatterns = [
    url(r'^$',
        PostListCreate.as_view(), name='api_post_list_create'),
    url(r'^(?P<post_id>\d+)/$',
        PostDetails.as_view(), name='api_post_details'),

    url(r'^(?P<post_id>\d+)/comment/$',
        PostCommentListCreate.as_view(), name='api_post_comment_list_create'),

]
