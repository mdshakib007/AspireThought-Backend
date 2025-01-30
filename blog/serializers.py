from rest_framework import serializers
from blog.models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'image', 'body', 'slug', 'created_at', 'updated_at', 'tags']
        read_only_fields = ['id', 'author', 'slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['slug'] = validated_data.get('title').replace(" ", "-").lower()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('slug', None)
        return super().update(instance, validated_data)
