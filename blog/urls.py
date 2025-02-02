from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import BlogViewSet, CreatePostAPIView, EditPostAPIView, DeletePostAPIView, LikeBlogView,  CommentCreateView, CommentListView 

router = DefaultRouter()
router.register('list', BlogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/', CreatePostAPIView.as_view(), name='create_post'),
    path('edit/', EditPostAPIView.as_view(), name='edit_post'),
    path('delete/', DeletePostAPIView.as_view(), name='delete_post'),
    path('<slug:slug>/like/', LikeBlogView.as_view(), name='like_post'),
    path('<slug:blog_slug>/comments/', CommentListView.as_view({'get': 'list'}), name='list_comments'),
    path('<slug:blog_slug>/comments/add/', CommentCreateView.as_view(), name='create_comment'),
]
