from typing import List

from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers.errors import (
    AuthenticationErrorSerializer,
    LoginValidationErrorSerializer,
    RegistrationValidationErrorSerializer,
)
from .serializers.user import UserLoginSerializer, UserRequestSerializer, UserResponseSerializer


class UserRegisterView(APIView):

    authentication_classes: List[BaseAuthentication] = []  # No authentication required for registration
    permission_classes: List[BasePermission] = [AllowAny]  # Allow any user to register

    @extend_schema(
        description="Create a new user",
        request=UserRequestSerializer,
        responses={201: UserResponseSerializer, 400: RegistrationValidationErrorSerializer},
    )
    def post(self, request: Request) -> Response:
        """
        Create a new user
        :param request: The request containing user details (email, username, first_name, last_name, password)
        :return: Response with status 201(created) and user data if successful, or error message if not.
        example:
        {
            "email": "user1@test.com",
            "username": "user1",
            "first_name": "Test",
            "last_name": "Test",
            "password": "user123"
        }
        """
        request_serializer = UserRequestSerializer(data=request.data)
        if request_serializer.is_valid():
            user = request_serializer.save()
            response_serializer = UserResponseSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    authentication_classes: List[BaseAuthentication] = []  # No authentication required for login
    permission_classes: List[BasePermission] = [AllowAny]  # Allow any user to log in

    @extend_schema(
        description="Login a user",
        request=UserLoginSerializer,
        responses={
            204: None,
            400: LoginValidationErrorSerializer,
            401: AuthenticationErrorSerializer,
        },
    )
    def post(self, request: Request) -> Response:
        """
        Log in a user
        :param request: The request containing user credentials (email and password)
        :return: Response with status 204(no content) and token in headers if successful, or error message if not
        example:
        {
            "email": "test@email.com",
            "password": "testpass123"
        }
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data["email"], password=serializer.validated_data["password"]
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)  # Get or create a token for the user
                return Response(
                    status=status.HTTP_204_NO_CONTENT,
                    headers={"Authorization": f"Token {token.key}"},
                )
            else:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
