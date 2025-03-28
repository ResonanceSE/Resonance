from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.auth_model import Token
from ..models.customer_model import Customer


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

        # username/email uniqueness
        if Customer.objects.filter(username=data["username"]).exists():
            return Response(
                {"status": "error", "message": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Customer.objects.filter(email=data["email"]).exists():
            return Response(
                {"status": "error", "message": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # password validation
        password = data["password"]
        password_errors = []

        # Check uppercase letter
        if not any(char.isupper() for char in password):
            password_errors.append(
                "Password must contain at least one uppercase letter."
            )

        # Check  number
        if not any(char.isdigit() for char in password):
            password_errors.append("Password must contain at least one number.")

        if password_errors:
            return Response(
                {"status": "error", "message": password_errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            password_validation.validate_password(data["password"])
        except ValidationError as e:
            return Response(
                {"status": "error", "message": e.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create user
        try:
            user = Customer.objects.create_user(
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
                        "phone_number": user.phone_number,
                        "address": user.get_full_address(),
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

        if not all(k in data for k in ["username", "password"]):
            return Response(
                {
                    "status": "error",
                    "message": "Username/email and password are required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        username_or_email = data["username"]
        password = data["password"]
        user = None
        user = authenticate(username=username_or_email, password=password)
        if user is None and "@" in username_or_email:
            try:
                user_obj = Customer.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
            except Customer.DoesNotExist:
                user = None

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
                        "phone_number": user.phone_number,
                        "address": user.get_full_address(),
                        "is_admin": user.is_superuser,
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
                    "phone_number": user.phone_number,
                    "address": user.get_full_address(),
                    "is_admin": user.is_superuser,
                },
            }
        )


class ValidatePasswordAPI(APIView):
    def post(self, request):
        data = request.data

        if "password" not in data:
            return Response(
                {"status": "error", "message": "Password is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        password = data["password"]
        password_errors = []

        if not any(char.isupper() for char in password):
            password_errors.append(
                "Password must contain at least one uppercase letter."
            )

        if not any(char.isdigit() for char in password):
            password_errors.append("Password must contain at least one number.")

        try:
            password_validation.validate_password(password)
        except ValidationError as e:
            password_errors.extend(e.messages)

        if password_errors:
            return Response(
                {"status": "error", "message": password_errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"status": "success", "message": "Password meets requirements"},
            status=status.HTTP_200_OK,
        )
