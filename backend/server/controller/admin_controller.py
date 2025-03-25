from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from ..models import Product, Order
from ..serializers import ProductSerializer


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_admin_stats(request):
    """Get sales statistics and analytics for admin dashboard"""
    # Get date range (default: last 30 days)
    days = int(request.GET.get("days", 30))
    start_date = timezone.now() - timedelta(days=days)

    # Calculate statistics
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
@permission_classes([IsAdminUser])
def manage_products(request, product_id=None):
    """Manage product listings - CRUD operations"""
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
@permission_classes([IsAdminUser])
def manage_orders(request, order_id=None):
    """Access and process orders"""
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


@api_view(["GET", "POST", "PUT"])
@permission_classes([IsAdminUser])
def manage_support_queries(request, query_id=None):
    """Handle customer support queries"""
    # This would integrate with your customer support system
    # For now, return a placeholder response
    return Response(
        {"message": "Support query management will be implemented in the next phase"}
    )
