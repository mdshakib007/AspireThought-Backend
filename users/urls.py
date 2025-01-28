from django.urls import path
from users.views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, activate, UserProfileUpdateAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('activate/<uid64>/<token>/', activate, name='activate'),
    path('login/', UserLoginAPIView.as_view(), name='user-register'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-register'),
    path('profile-update/', UserProfileUpdateAPIView.as_view(), name='user-profile-update'),
]
