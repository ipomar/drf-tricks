from rest_framework import serializers

from apps.comments.models import Comment
from apps.posts.api.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'author', 'created_on', 'text', 'is_banned']
        read_only_fields = ['is_banned']


class CommentBannedSerializer(serializers.ModelSerializer):

    banned_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['banned', 'banned_on', 'banned_by']
