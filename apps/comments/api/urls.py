from django.conf.urls import url

from apps.comments.api.views import CommentDetails, CommentBannedDetails

# /api/comment/...

urlpatterns = [
    url(r'^(?P<comment_id>\d+)/$',
        CommentDetails.as_view(), name='api_comment_details'),
    url(r'^(?P<comment_id>\d+)/banned/$',
        CommentBannedDetails.as_view(), name='api_comment_banned_details'),

]
