from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework.filters import BaseFilterBackend
from blog.models import Blog
from blog.serializers import BlogSerializer
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
        post_id = self.request.query_params.get('post_id')
        author_id = self.request.query_params.get('author_id')
        tag_id = self.request.query_params.get('tag_id')
        title = self.request.query_params.get('title')

        if post_id:
            queryset = queryset.filter(id=post_id)
        if author_id:
            queryset = queryset.filter(author = author_id)
        if tag_id:
            queryset = queryset.filter(tags=tag_id)
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
        post_id = request.data.get('post_id')

        try:
            post = Blog.objects.get(id=post_id, user=user)
        except Blog.DoesNotExist:
            return ValidationError({"error" : "Post does not found"})

        post.delete()
        return Response({"success" : "Post deleted successfully"})


class EditPostAPIView(APIView):
    def post(self, request):
        user = request.user
        post_id = request.data.get('post_id')

        try:
            post = Blog.objects.get(id=post_id, user=user)
        except Blog.DoesNotExist:
            return ValidationError({"error" : "Post does not found"})

        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success" : "Post updated successfully"})
        return Response(serializer.errors)

