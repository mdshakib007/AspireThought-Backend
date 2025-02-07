from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, activate, UserProfileUpdateAPIView, UserViewSet, BookmarkAPIView, RequestVerification, FollowingAPIView

router = DefaultRouter()
router.register("list", UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('activate/<uid64>/<token>/', activate, name='activate'),
    path('login/', UserLoginAPIView.as_view(), name='user-register'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-register'),
    path('update/', UserProfileUpdateAPIView.as_view(), name='user-profile-update'),
    path('bookmark/add/', BookmarkAPIView.as_view(), name='add-bookmark'),
    path('bookmark/remove/', BookmarkAPIView.as_view(), name='remove-bookmark'),
    path('following/topic/add/', FollowingAPIView.as_view(), name='add-following'),
    path('following/topic/remove/', FollowingAPIView.as_view(), name='remove-following'),
    path('request-verification/', RequestVerification.as_view(), name='request-verification'),
]
