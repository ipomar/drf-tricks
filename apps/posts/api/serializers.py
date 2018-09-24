from rest_framework import serializers

from apps.posts.models import Post


class PostContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        exclude_fields = [
            'is_banned', 'banned_by', 'banned_on'
        ]


class PostBanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['is_banned', 'banned_by', 'banned_on']
        read_only_fields = ['banned_by', 'banned_on']
