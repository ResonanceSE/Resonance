from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.auth_model import Token


class RegisterAPI(APIView):
    def post(self, request):
        data = request.data

        # Check required fields
        if not all(k in data for k in ["username", "password", "email"]):
            return Response(
                {
                    "status": "error",
                    "message": "Username, password and email are required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check username/email uniqueness
        if User.objects.filter(username=data["username"]).exists():
            return Response(
                {"status": "error", "message": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=data["email"]).exists():
            return Response(
                {"status": "error", "message": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create user
        try:
            
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
            )

            token = Token.objects.create(user=user)

            return Response(
                {
                    "status": "success",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "token": token.key,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginAPI(APIView):
    def post(self, request):
        data = request.data

        # Check required fields
        if not all(k in data for k in ["username", "password"]):
            return Response(
                {"status": "error", "message": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authenticate
        user = authenticate(username=data["username"], password=data["password"])

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "status": "success",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "token": token.key,
                    },
                }
            )
        else:
            return Response(
                {"status": "error", "message": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({"status": "success"})


class UserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "status": "success",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            }
        )
