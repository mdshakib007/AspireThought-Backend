from django.urls import path
from .views import BlogListCreateAPIView, BlogDetailAPIView

urlpatterns = [
    path('list/', BlogListCreateAPIView.as_view(), name='blog-list-create'),
    path('entry/<slug:slug>/', BlogDetailAPIView.as_view(), name='blog-detail'),
]
