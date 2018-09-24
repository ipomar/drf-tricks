from django.conf.urls import url

from apps.posts.api.views import PostListCreate, PostDetails, PostBanDetails, PostDeleteDetails

# /api/post/...

urlpatterns = [
    url(r'^$',
        PostListCreate.as_view(), name='api_post_list_create'),
    url(r'^(?P<post_id>\d+)/',
        PostDetails.as_view(), name='api_post_details'),
    url(r'^(?P<post_id>\d+)/banned/',
        PostBanDetails.as_view(), name='api_post_banned_details'),

    url(r'^(?P<post_id>\d+)/comment/$',
        PostCommentListCreate.as_view(), name='api_post_comment_list_create'),
]
