from rest_framework import views, viewsets
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from . import models
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from . import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import CustomUser, UserProfile
from .permissions import SuperUserPermission,UserPermission


class LoginViewSet(views.APIView):

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=serializers.LoginSerializer)
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({'msg': 'Please provide both username and password'},status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=email, password=password)
        if not user:
            return Response({'msg': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
        if not user.is_active:
            return Response({'msg': 'User is inactive. Please contact admin.'}, status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'is_ngo': user.is_ngo}, status=HTTP_200_OK)

class RegisterViewSet(views.APIView):

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=serializers.RegisterSerializer)
    def post(self, request):

        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'msg': 'User successfully created'}, status=HTTP_200_OK)

class UserProfileViewSet(views.APIView):

    permission_classes = [UserPermission]

    def get(self, request):

        userProfile = UserProfile.objects.get(pk=request.user)
        serializer = serializers.UserProfileSerailizer(userProfile)
        
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.UserProfileSerailizer)
    def put(self, request, pk=None):

        userProfile = UserProfile.objects.get(pk=request.user)

        serializer = serializers.UserProfileSerailizer(userProfile,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'msg': 'User profile successfully updated'}, status=HTTP_200_OK)








    
    
    


