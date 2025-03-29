from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.auth_model import Token
from ..models.user_model import User


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

        user_type = data.get("user_type", "customer").lower()

        if user_type == "admin" and not (
            request.user and request.user.is_authenticated and request.user.is_superuser
        ):
            return Response(
                {"status": "error", "message": "Unauthorized to create admin users"},
                status=status.HTTP_403_FORBIDDEN,
            )

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

        # Password validation (unchanged)
        password = data["password"]
        password_errors = []

        if not any(char.isupper() for char in password):
            password_errors.append(
                "Password must contain at least one uppercase letter."
            )

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

        try:
            user_data = {
                "username": data["username"],
                "email": data["email"],
                "password": data["password"],
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
            }

            if user_type == "admin":
                user = User.objects.create_user(**user_data)
                user.is_staff = True
                user.save()
            else:
                user = User.objects.create_user(**user_data)

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
                        "user_type": user_type,
                        "is_admin": user_type == "admin",
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
        print("LOGIN REQUEST DATA:", data)

        if not all(k in data for k in ["username", "password"]):
            return Response(
                {
                    "status": "error",
                    "message": "Username/email and password are required",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        username_or_email = data.get("username", "")
        password = data.get("password", "")

        print(f"Attempting to authenticate: {username_or_email}")

        try:
            user = User.objects.get(username=username_or_email)
            if not user.check_password(password):
                user = None
                print("Password check failed")
            else:
                print("Authentication successful by username")
        except User.DoesNotExist:
            if "@" in username_or_email:
                try:
                    user = User.objects.get(email=username_or_email)
                    if not user.check_password(password):
                        user = None
                        print("Password check failed for email user")
                    else:
                        print("Authentication successful by email")
                except User.DoesNotExist:
                    user = None
                    print("No user found with this email")
            else:
                user = None
                print("No user found with this username")

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
                        "is_admin": user.is_staff,
                        "is_superuser": user.is_superuser,
                        "user_type": "admin" if user.is_staff else "customer",
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
                    "is_admin": user.is_staff,  # Changed from is_superuser to is_staff
                    "user_type": "admin"
                    if user.is_staff
                    else "customer",  # Added user_type
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


class UpdateAddressAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        if "address" not in data:
            return Response(
                {"status": "error", "message": "Address is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Update address fields
            address = data["address"]

            # Split the address to update the fields
            address_parts = address.split("\n")

            # Update user fields
            if len(address_parts) >= 1:
                user.address = address

            # Extract city, state, postal code
            if len(address_parts) >= 4:
                address_line = address_parts[3]
                parts = address_line.split(",")
                if len(parts) >= 1:
                    user.city = parts[0].strip()

                if len(parts) >= 2:
                    state_zip = parts[1].strip().split(" ", 1)
                    if len(state_zip) >= 1:
                        user.state = state_zip[0]
                    if len(state_zip) >= 2:
                        user.postal_code = state_zip[1]

            # Extract country
            if len(address_parts) >= 5:
                user.country = address_parts[4]

            user.save()

            return Response(
                {
                    "status": "success",
                    "message": "Address updated successfully",
                    "data": {
                        "address": user.address,
                    },
                }
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UpdateUsernameAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        if "username" not in data:
            return Response(
                {"status": "error", "message": "Username is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_username = data["username"]
        if User.objects.filter(username=new_username).exclude(id=user.id).exists():
            return Response(
                {"status": "error", "message": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user.username = new_username
            user.save()

            return Response(
                {
                    "status": "success",
                    "message": "Username updated successfully",
                    "data": {
                        "username": user.username,
                    },
                }
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
