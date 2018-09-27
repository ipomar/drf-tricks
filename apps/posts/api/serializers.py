from django.contrib.auth.models import User
from rest_framework import serializers

from apps.posts.api.fields import CategorySerializerField
from apps.posts.models import Post, Category


class UserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name']

    def get_name(self, instance):
        return ' '.join([
            w for w in
            [instance.first_name, instance.last_name]
            if w
        ])


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class PostContentSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)
    category = CategorySerializerField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'created_on', 'title', 'text', 'category']
