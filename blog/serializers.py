from rest_framework import serializers
from blog.models import Blog, Like, Comment


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'blog', 'created_at']
        read_only_fields = ['created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'blog', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'blog', 'created_at']


class BlogSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['title', 'slug', 'author', 'image', 'body', 'tags', 'created_at', 'updated_at', 'like_count', 'comment_count']
        read_only_fields = ['slug', 'author', 'created_at', 'updated_at', 'like_count', 'comment_count']

    def get_like_count(self, obj):
        return obj.like_count()

    def get_comment_count(self, obj):
        return obj.comment_count()

