from rest_framework import serializers
from blog.models import Blog
from blog.models import Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'blog', 'created_at']
        read_only_fields = ['created_at']

class BlogSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['title', 'slug', 'author', 'image', 'body', 'tags', 'created_at', 'updated_at', 'like_count']

    def get_like_count(self, obj):
        return obj.like_count()
