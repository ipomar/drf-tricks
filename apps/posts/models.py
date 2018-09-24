from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='posts')
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    text = models.TextField(validators=[MaxLengthValidator(50000)])

    class Meta:
        ordering = ['-id']
