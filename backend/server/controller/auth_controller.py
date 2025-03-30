from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.utils.html import format_html
import uuid
import re

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models.auth_model import Token
from ..models.user_model import User


@api_view(["POST"])
def register(request):
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
    user_is_superuser = data.get("is_superuser", False)

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

    # Password validation
    password = data["password"]
    password_errors = []

    if not any(char.isupper() for char in password):
        password_errors.append("Password must contain at least one uppercase letter.")

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
            if user_is_superuser:
                user.is_superuser = True
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
                    "address": user.get_full_address(),
                    "user_type": user_type,
                    "is_admin": user_type == "admin",
                    "is_superuser": user.is_superuser,
                },
            },
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response(
            {"status": "error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def login(request):
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return Response({"status": "success"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
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
                "address": user.get_full_address(),
                "is_admin": user.is_staff,
                "user_type": "admin" if user.is_staff else "customer",
            },
        }
    )


@api_view(["POST"])
def validate_password(request):
    data = request.data

    if "password" not in data:
        return Response(
            {"status": "error", "message": "Password is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    password = data["password"]
    password_errors = []

    if not any(char.isupper() for char in password):
        password_errors.append("Password must contain at least one uppercase letter.")

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


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_address(request):
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


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data

    # Validate input
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
        # Update user profile data
        user.username = new_username

        if "first_name" in data:
            user.first_name = data["first_name"]

        if "last_name" in data:
            user.last_name = data["last_name"]

        user.save()

        return Response(
            {
                "status": "success",
                "message": "Profile updated successfully",
                "data": {
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            }
        )
    except Exception as e:
        return Response(
            {"status": "error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def forgot_password(request):
    """
    Process forgot password request and send reset email
    """
    data = request.data

    if "email" not in data:
        return Response(
            {"status": "error", "message": "Email address is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    email = data["email"].lower().strip()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return Response(
            {"status": "error", "message": "Invalid email format"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {
                "status": "success",
                "message": "If your email is registered, you will receive reset instructions shortly.",
            },
            status=status.HTTP_200_OK,
        )

    # Generate reset token
    reset_token = uuid.uuid4().hex

    # Set reset token and expiration
    user.reset_token = reset_token
    user.reset_token_expiry = timezone.now() + timedelta(hours=24)
    user.save()
    reset_url = f"{settings.FRONTEND_URL}/reset_password?token={reset_token}"
    email_body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Password Reset</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #4a6ee0;">Resonance Sound Shop</h2>
                <div style="height: 3px; background-color: #f97316; width: 100px; margin: 0 auto;"></div>
            </div>
            
            <p>Hello {user.first_name or user.username},</p>
            
            <p>We received a request to reset the password for your Resonance Sound Shop account.</p>
            
            <div style="margin: 30px 0; text-align: center;">
                <a href="{reset_url}" style="background-color: #f97316; color: white; padding: 12px 20px; text-decoration: none; border-radius: 4px; font-weight: bold; display: inline-block;">Reset Your Password</a>
            </div>
            
            <p>If you didn't request this password reset, you can safely ignore this email - your account is secure.</p>
            
            <p>This link will expire in 24 hours.</p>
            
            <p>Best regards,<br>
            The Resonance Sound Shop Team</p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #777;">
                <p>This is an automated message, please do not reply to this email.</p>
                <p>&copy; 2025 Resonance Sound Shop. All rights reserved.</p>
            </div>
        </body>
        </html>
    """
    email_body = f"""
        Hello {user.first_name or user.username},

        You recently requested to reset your password for your Resonance Sound Shop account.

        Your password reset link is below:
        {reset_url}

        This link will expire in 24 hours.

        If you did not request this password reset, no action is needed.

        Regards,
        Resonance Sound Shop
    """

    # Send email
    try:
        email_message = EmailMessage(
        subject="Reset Your Resonance Sound Shop Password",
        body=email_body, 
        from_email=f"Resonance Sound Shop <{settings.DEFAULT_FROM_EMAIL}>",
        to=[email],
    )
        email_message.content_subtype = "html"
        email_message.body = email_body_html 
        email_message.extra_headers = {
            "X-Priority": "1",
            "X-MSMail-Priority": "High",
            "Importance": "High",
            "X-Auto-Response-Suppress": "OOF, DR, AutoReply"
        }
        email_message.send(fail_silently=False)

    except Exception as e:
        return Response(
            {"status": "error", "message": f"Failed to send email: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(
        {
            "status": "success",
            "message": "Password reset instructions have been sent to your email.",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def reset_password(request):
    """
    Process password reset using token
    """
    data = request.data

    if not all(k in data for k in ["token", "password"]):
        return Response(
            {"status": "error", "message": "Token and new password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    token = data["token"]
    new_password = data["password"]

    try:
        user = User.objects.get(reset_token=token)
    except User.DoesNotExist:
        return Response(
            {"status": "error", "message": "Invalid or expired token"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if token is expired
    if not user.reset_token_expiry or user.reset_token_expiry < timezone.now():
        return Response(
            {"status": "error", "message": "Reset token has expired"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate new password
    try:
        password_validation.validate_password(new_password, user)
    except ValidationError as e:
        return Response(
            {"status": "error", "message": e.messages},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(new_password)

    user.reset_token = None
    user.reset_token_expiry = None
    user.save()

    return Response(
        {
            "status": "success",
            "message": "Your password has been reset successfully",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def validate_reset_token(request):
    """
    Validate a password reset token
    """
    data = request.data
    if "token" not in data:
        return Response(
            {"status": "error", "message": "Token is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    token = data["token"]
    try:
        user = User.objects.get(reset_token=token)

        if not user.reset_token_expiry or user.reset_token_expiry < timezone.now():
            return Response(
                {"status": "error", "message": "Reset token has expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "status": "success",
                "message": "Token is valid",
                "username": user.username,
            },
            status=status.HTTP_200_OK,
        )
    except User.DoesNotExist:
        return Response(
            {"status": "error", "message": "Invalid token"},
            status=status.HTTP_400_BAD_REQUEST,
        )
