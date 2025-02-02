from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import BaseFilterBackend
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from users.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, BookmarkSerializer
from blog.models import Blog  





class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            # Generate token for email confirmation
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://aspirethought-backend.onrender.com/user/activate/{uid}/{token}"
            
            # Send confirmation email
            email_sub = "Confirm Your Email"
            email_body = render_to_string('users/confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_sub, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()

            return Response({"success": "Please check your email for confirmation!"})

        return Response(serializer.errors)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = get_user_model()._default_manager.get(pk=uid)
    except(get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "users/email_confirmed.html")
    else:
        return Response({"error": "Something went wrong"})


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response({'error' : 'Invalid information provided!'})
        return Response(serializer.errors)


class UserLogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'success': 'Logout successful!'}, status=200)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found.'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500) 


class UserProfileUpdateAPIView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user = request.user 
        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Profile updated successfully!"})

        return Response(serializer.errors)


class SpecificUser(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        uid = request.query_params.get("user_id")
        username = request.query_params.get("username")

        if uid:
            return queryset.filter(id=uid)
        if username:
            return queryset.filter(username=username)
        return queryset

class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = get_user_model().objects.all()
    filter_backends = [SpecificUser]


class BookmarkAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        slug = request.data.get('slug')

        try:
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            return Response({"error": "Blog post does not exist."})

        if slug not in user.bookmarks:
            user.bookmarks.append(slug)
            user.save()
            return Response({"success": "Blog added to bookmarks."})
        
        return Response({"error": "Blog already in bookmarks."})

    def delete(self, request):
        user = request.user
        slug = request.data.get('slug')

        try:
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            return Response({"error": "Blog post does not exist."})

        if slug in user.bookmarks:
            user.bookmarks.remove(slug)
            user.save()
            return Response({"success": "Blog removed from bookmarks."})
        
        return Response({"error": "Blog not in bookmarks."})


class RequestVerification(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if not user.verification_requested:
            user.verification_requested = True
            user.save()
            return Response({"success" : "Your request for verification is pending!"})
            
        return Response({"error" : "You already requested for verification!"})
    