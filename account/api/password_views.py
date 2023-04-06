# REST FRAMEWORK
from rest_framework.response import Response
from rest_framework import status

# REST FRAMEWORK VIEWS
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView

# PERMISSIONS
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

# MODELS
from account.models import User

# PASSWORD - EMAIL
from django.contrib.auth.hashers import make_password, check_password
# EMAIL
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from account.api.password_serializers import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    NewPasswordSerializer
)

# CHANGE PASSWORD
class ChangePasswordView(UpdateAPIView):
    """
    A endpoint for changing password
    """
    # queryset = User.object.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        # serializer = self.get_serializer(data=request.data)
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            
            # Check old_password
            # self.object -> user
            valid = self.object.check_password(serializer.data.get('old_password'))
            if not valid:
                return Response({"old_password": "Old password is not correct"}, status=status.HTTP_400_BAD_REQUEST)
            
            # New passwords Match
            # new_password = serializer.data.get('new_password')
            # new_password_confirm = serializer.data.get('new_password_confirm')
            # if new_password != new_password_confirm:
            #     return Response({"new_password": "Password fields didn't match."}, status=status.HTTP_400_BAD_REQUEST)
                
            # set_password
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }

            # serializer.save()

            return Response(response, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
# ::VERSION 1
class PasswordResetEmailAPIView(CreateAPIView):
    """
    A endpoint for sending email with token
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer
    model = User

    def get_object(self):
        obj = self.request.user
        return obj
    
    def create(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # print(self.object)
            # -> AnonymousUser

            user_email = serializer.data.get('email')
            user = User.objects.get(email=user_email)
            
            # print(user)
            # -> user email (uberke.karatas@gmail.com)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)

            message = render_to_string('password-reset-email.html', {
                'user': user,
                'uid': uid,
                'token': token
            })

            to_email = user.email
            email = EmailMessage(
                'Password Reset',
                message,
                to=[to_email]
            )

            email.send()
            
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Email send successfully',
                'email': user.email,
                'uid': uid,
                'token': token
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordResetTokenCheckAPIView(APIView):
    def get(self, request, uidb64, token):
        # Try-Except ?

        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
        
        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Credentials Valid',
                'email': user.email,
                'uid': uidb64,
                'token': token
        }

        return Response(response, status=status.HTTP_200_OK)

class SetNewPasswordAPIView(UpdateAPIView):
    serializer_class = NewPasswordSerializer
    model = User
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            uidb64 = serializer.data.get('uidb64')
            token = serializer.data.get('token')

            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.data.get('new_password'))
            user.save()

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }

            return Response(response, status=status.HTTP_200_OK)