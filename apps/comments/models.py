from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone


class Comment(models.Model):
    post = models.ForeignKey(to='posts.Post')
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comments')
    created_on = models.DateTimeField(auto_now_add=True)
    text = models.TextField(validators=[MaxLengthValidator(2000)])

    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='deleted_comments')
    deleted_on = models.DateTimeField(null=True)

    is_banned = models.BooleanField(default=False)
    banned_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='banned_comments')
    banned_on = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.is_deleted:
            if not self.deleted_by:
                raise RuntimeError("'deleted_by' not set when 'is_deleted' is True")
            self.deleted_on = self.deleted_on or timezone.datetime.now()

        if self.is_banned:
            if not self.banned_by:
                raise RuntimeError("'banned_by' not set when 'is_banned' is True")
            self.banned_on = self.banned_by or timezone.datetime.now()

        super().save(*args, **kwargs)
