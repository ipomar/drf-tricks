from rest_framework import serializers


class CategorySerializerField(serializers.Field):

    def to_representation(self, value):
        from apps.posts.api.serializers import CategorySerializer
        return CategorySerializer(value).data

    def to_internal_value(self, data):
        from apps.posts.models import Category
        category_id = data.get('id') if type(data) == dict else None
        return Category.objects.filter(id=category_id).first()
