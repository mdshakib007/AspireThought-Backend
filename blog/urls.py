from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import BlogViewSet, CreatePostAPIView, EditPostAPIView, DeletePostAPIView


router = DefaultRouter()
router.register('list', BlogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/', CreatePostAPIView.as_view(), name='create_post'),
    path('edit/', EditPostAPIView.as_view(), name='edit_post'),
    path('delete/', DeletePostAPIView.as_view(), name='delete_post'),
]
