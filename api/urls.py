from django.conf.urls import url, include


urlpatterns = [
    url(r'^post/', include('apps.posts.api.urls')),
    url(r'^comment/', include('apps.comments.api.urls')),
]
