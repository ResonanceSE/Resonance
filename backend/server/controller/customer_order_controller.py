from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import uuid
from decimal import Decimal
from ..models import Order, OrderItem, Product, Customer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    """
    Create a new order from the items provided in the request
    """
    user = request.user
    data = request.data

    # Check if we have the required data
    if not data.get("shipping_address"):
        return Response(
            {"status": "error", "message": "Shipping address is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    items_data = data.get("items")
    if not items_data:
        return Response(
            {"status": "error", "message": "No cart found and no cart items provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        with transaction.atomic():
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"

            total_amount = Decimal("0.00")

            # Create order
            order = Order.objects.create(
                user=user,
                order_number=order_number,
                shipping_address=data["shipping_address"],
                total_amount=total_amount,
                payment_status=False,
            )

            # Process items
            for item_data in items_data:
                product_id = item_data.get("product_id")
                quantity = item_data.get("quantity", 1)
                price = (
                    Decimal(str(item_data.get("price"))) / 100
                ) 

                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    raise ValueError(f"Product with ID {product_id} not found")

                OrderItem.objects.create(
                    order=order, product=product, quantity=quantity, price=price
                )

                total_amount += price * quantity

            order.total_amount = total_amount
            order.save()

            return Response(
                {
                    "status": "success",
                    "message": "Order created successfully",
                    "data": {
                        "order_id": order.id,
                        "order_number": order.order_number,
                        "total_amount": str(order.total_amount),
                    },
                },
                status=status.HTTP_201_CREATED,
            )

    except ValueError as e:
        return Response(
            {"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"status": "error", "message": f"Failed to create order: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_user_by_id(request, user_id):
    try:
        user = Customer.objects.get(id=user_id)
        return Response({"id": user.id, "username": user.username, "email": user.email})
    except Customer.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    """Get all orders for the authenticated user"""
    user = request.user
    orders = Order.objects.filter(user=user).order_by("-created_at")

    orders_data = []
    for order in orders:
        order_items = []
        for item in order.items.all():
            order_items.append(
                {
                    "product": item.product.name,
                    "quantity": item.quantity,
                    "price": str(item.price),
                    "subtotal": str(item.price * item.quantity),
                }
            )

        orders_data.append(
            {
                "id": order.id,
                "order_number": order.order_number,
                "status": order.status,
                "total_amount": str(order.total_amount),
                "shipping_address": order.shipping_address,
                "payment_status": order.payment_status,
                "created_at": order.created_at,
                "items": order_items,
            }
        )

    return Response(
        {"status": "success", "data": orders_data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_details(request, order_id):
    """Get details of a specific order"""
    user = request.user

    try:
        # Ensure the order belongs to the authenticated user
        order = Order.objects.get(id=order_id, user=user)

        order_items = []
        for item in order.items.all():
            order_items.append(
                {
                    "product": item.product.name,
                    "quantity": item.quantity,
                    "price": str(item.price),
                    "subtotal": str(item.price * item.quantity),
                }
            )

        order_data = {
            "id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "total_amount": str(order.total_amount),
            "shipping_address": order.shipping_address,
            "payment_status": order.payment_status,
            "created_at": order.created_at,
            "items": order_items,
        }

        return Response(
            {"status": "success", "data": order_data},
            status=status.HTTP_200_OK,
        )
    except Order.DoesNotExist:
        return Response(
            {"status": "error", "message": "Order not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
