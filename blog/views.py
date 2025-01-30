from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Blog
from .serializers import BlogSerializer
from django.shortcuts import get_object_or_404

class BlogListCreateAPIView(APIView):
    def get(self, request):
        blogs = Blog.objects.all().order_by('-created_at')
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogDetailAPIView(APIView):
    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        blog.delete()
        return Response({"message": "Blog deleted"}, status=status.HTTP_204_NO_CONTENT)
