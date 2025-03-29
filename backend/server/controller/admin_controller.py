from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from ..models import Product, Order, Category, User, AdminStaff
from ..serializers import ProductSerializer, CategorySerializer


@api_view(["GET"])
def get_admin_stats(request):
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED
        )

    if not (request.user.is_staff or request.user.is_superuser):
        return Response(
            {"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN
        )

    days = int(request.GET.get("days", 30))
    start_date = timezone.now() - timedelta(days=days)

    stats = {
        "total_sales": Order.objects.filter(
            created_at__gte=start_date, status="delivered"
        ).aggregate(total=Sum("total_amount"))["total"]
        or 0,
        "total_orders": Order.objects.filter(created_at__gte=start_date).count(),
        "pending_orders": Order.objects.filter(status="pending").count(),
        "low_stock_products": Product.objects.filter(stock__lt=10).count(),
    }

    return Response({"status": "success", "data": stats})


@api_view(["GET", "POST", "PUT", "DELETE"])
def manage_products(request, product_id=None):
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED
        )

    if not (request.user.is_staff or request.user.is_superuser):
        return Response(
            {"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "GET":
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

    elif request.method == "DELETE":
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )


@api_view(["GET", "PUT"])
def manage_orders(request, order_id=None):
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED
        )

    if not (request.user.is_staff or request.user.is_superuser):
        return Response(
            {"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN
        )

    if request.method == "GET":
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                return Response(
                    {
                        "id": order.id,
                        "order_number": order.order_number,
                        "status": order.status,
                        "total_amount": str(order.total_amount),
                        "shipping_address": order.shipping_address,
                        "created_at": order.created_at,
                        "items": [
                            {
                                "product": item.product.name,
                                "quantity": item.quantity,
                                "price": str(item.price),
                            }
                            for item in order.items.all()
                        ],
                        "user": order.user.username,
                    }
                )
            except Order.DoesNotExist:
                return Response(
                    {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            orders = Order.objects.all().order_by("-created_at")
            return Response(
                [
                    {
                        "id": order.id,
                        "order_number": order.order_number,
                        "status": order.status,
                        "total_amount": str(order.total_amount),
                        "created_at": order.created_at,
                        "user": order.user.username,
                    }
                    for order in orders
                ]
            )

    elif request.method == "PUT":
        try:
            order = Order.objects.get(id=order_id)
            # Only allow updating order status
            new_status = request.data.get("status")
            if new_status in [s[0] for s in Order.STATUS_CHOICES]:
                order.status = new_status
                order.save()
                return Response(
                    {
                        "id": order.id,
                        "order_number": order.order_number,
                        "status": order.status,
                    }
                )
            return Response(
                {"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )


@api_view(["GET"])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_staff_list(request):
    """Get a list of all admin staff members"""
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED
        )

    if not (request.user.is_staff or request.user.is_superuser):
        return Response(
            {"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN
        )

    # Get all staff members using AdminStaff proxy model
    try:
        staff_members = AdminStaff.objects.all()

        staff_data = [
            {
                "id": staff.id,
                "username": staff.username,
                "email": staff.email,
                "first_name": staff.first_name,
                "last_name": staff.last_name,
                "is_superuser": staff.is_superuser,
                "created_at": staff.created_at,
            }
            for staff in staff_members
        ]

        return Response(
            {"status": "success", "data": staff_data},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"status": "error", "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET", "PUT", "DELETE"])
def manage_staff(request, staff_id):
    """Get, update or delete a staff member"""
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED
        )

    if not (request.user.is_staff or request.user.is_superuser):
        return Response(
            {"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN
        )

    try:
        staff = AdminStaff.objects.get(id=staff_id)
    except AdminStaff.DoesNotExist:
        return Response(
            {"status": "error", "message": "Staff member not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.method == "GET":
        staff_data = {
            "id": staff.id,
            "username": staff.username,
            "email": staff.email,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "is_superuser": staff.is_superuser,
            "created_at": staff.created_at,
        }

        return Response(
            {"status": "success", "data": staff_data},
            status=status.HTTP_200_OK,
        )

    # PUT request - update staff details
    elif request.method == "PUT":
        data = request.data

        # Update basic fields
        if "username" in data and data["username"] != staff.username:
            # Check if username is already taken
            if (
                User.objects.filter(username=data["username"])
                .exclude(id=staff_id)
                .exists()
            ):
                return Response(
                    {"status": "error", "message": "Username already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            staff.username = data["username"]

        if "email" in data and data["email"] != staff.email:
            # Check if email is already taken
            if User.objects.filter(email=data["email"]).exclude(id=staff_id).exists():
                return Response(
                    {"status": "error", "message": "Email already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            staff.email = data["email"]

        # Update name fields
        if "first_name" in data:
            staff.first_name = data["first_name"]

        if "last_name" in data:
            staff.last_name = data["last_name"]

        # Update password if provided
        if "password" in data and data["password"]:
            try:
                validate_password(data["password"])
                staff.set_password(data["password"])
            except ValidationError as e:
                return Response(
                    {"status": "error", "message": e.messages},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        staff.save()

        return Response(
            {"status": "success", "message": "Staff member updated successfully"},
            status=status.HTTP_200_OK,
        )

    # DELETE request - remove staff member
    elif request.method == "DELETE":
        # Prevent self-deletion
        if staff.id == request.user.id:
            return Response(
                {"status": "error", "message": "You cannot delete your own account"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Delete the staff member
        staff.delete()

        return Response(
            {"status": "success", "message": "Staff member deleted successfully"},
            status=status.HTTP_200_OK,
        )
