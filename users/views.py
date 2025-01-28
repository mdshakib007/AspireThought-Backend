from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from users.serializers import UserRegistrationSerializer, UserLoginSerializer, UserLogoutSerializer, UserProfileUpdateSerializer



class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            # Generate token for email confirmation
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/user/activate/{uid}/{token}"
            
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
    serializer_class = UserLogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            token_key = serializer.validated_data['token']
            user_id = serializer.validated_data['user_id']

            try:
                token = Token.objects.get(key=token_key)
                if token.user.id == user_id:
                    # Delete the token to log the user out
                    token.delete()
                    return Response({'success': 'Logout successful!'})
                else:
                    return Response({'error': 'Invalid token for the given user.'})
            except Token.DoesNotExist:
                return Response({'error': 'Token not found.'})

        return Response(serializer.errors)

class UserProfileUpdateAPIView(APIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user 
        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Profile updated successfully!"})
        
        return Response(serializer.errors)
