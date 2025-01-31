from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework.filters import BaseFilterBackend
from blog.models import Blog, Like
from blog.serializers import BlogSerializer, LikeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.validators import ValidationError


class BlogPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BlogViewSet(ReadOnlyModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.all().order_by('-created_at')
    pagination_class = BlogPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        # get all filter parameters
        post_slug = self.request.query_params.get('post_slug')
        author_id = self.request.query_params.get('author_id')
        tag_slug = self.request.query_params.get('tag_slug')
        title = self.request.query_params.get('title')

        if post_slug:
            queryset = queryset.filter(id=post_slug)
        if author_id:
            queryset = queryset.filter(author = author_id)
        if tag_slug:
            queryset = queryset.filter(tags=tag_slug)
        if title:
            queryset = queryset.filter(title__icontains = title)

        return queryset
    

class CreatePostAPIView(APIView):
    serializer_class = BlogSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            blog = serializer.save(author=user)
            return Response({"success" : "Blog created successfully!"})
        
        return Response(serializer.errors)


class DeletePostAPIView(APIView):
    def post(self, request):
        user = request.user
        post_slug = request.data.get('post_slug')

        try:
            post = Blog.objects.get(slug=post_slug, user=user)
        except Blog.DoesNotExist:
            return ValidationError({"error" : "Post does not found"})

        post.delete()
        return Response({"success" : "Post deleted successfully"})


class EditPostAPIView(APIView):
    def post(self, request):
        user = request.user
        post_slug = request.data.get('post_slug')

        try:
            post = Blog.objects.get(slug=post_slug, user=user)
        except Blog.DoesNotExist:
            return ValidationError({"error" : "Post does not found"})

        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success" : "Post updated successfully"})
        return Response(serializer.errors)


class LikeBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        try:
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found"})

        like, created = Like.objects.get_or_create(user=request.user, blog=blog)

        if not created:
            like.delete()
            return Response({"message": "Blog unliked"})

        return Response({"message": "Blog liked"})
