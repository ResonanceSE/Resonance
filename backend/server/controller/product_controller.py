from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework import status
from server.models import Product, Category
from server.serializers import ProductSerializer
from django.conf import settings
import requests

class initializeController_Product:
    def __str__(self):
        return "Initialize Controller"


@api_view(["GET"])
def get_all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_product_by_category(request, category):
    try:
        category_obj = Category.objects.get(slug=category)
        products = Product.objects.filter(category=category_obj)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=404)


@api_view(["GET"])
def get_product_detailed(request, category, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def get_product_detailed_single_route(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def get_product_filters(request):
    """
    Get unique filter options for the product filters
    Returns all unique brands, connection types, etc. from the products database
    """
    # Get unique brands and count of products for each
    brands = (
        Product.objects.values("brand").annotate(count=Count("brand")).order_by("brand")
    )

    # Get unique connection types and count of products for each
    connections = (
        Product.objects.values("connections")
        .annotate(count=Count("connections"))
        .order_by("connections")
    )

    # Get price ranges (calculated on the fly)
    price_min = (
        Product.objects.order_by("price").first().price
        if Product.objects.exists()
        else 0
    )
    price_max = (
        Product.objects.order_by("-price").first().price
        if Product.objects.exists()
        else 1000
    )

    # Create price ranges based on actual data
    price_ranges = []
    if Product.objects.exists():
        # Define price ranges
        if price_min < 100:
            price_ranges.append(
                {
                    "name": "Under $100",
                    "min": 0,
                    "max": 99.99,
                    "count": Product.objects.filter(price__lt=100).count(),
                }
            )

        if price_min < 300 and price_max > 100:
            price_ranges.append(
                {
                    "name": "$100 - $300",
                    "min": 100,
                    "max": 299.99,
                    "count": Product.objects.filter(
                        price__gte=100, price__lt=300
                    ).count(),
                }
            )

        if price_min < 500 and price_max > 300:
            price_ranges.append(
                {
                    "name": "$300 - $500",
                    "min": 300,
                    "max": 499.99,
                    "count": Product.objects.filter(
                        price__gte=300, price__lt=500
                    ).count(),
                }
            )

        if price_max > 500:
            price_ranges.append(
                {
                    "name": "Over $500",
                    "min": 500,
                    "max": None,
                    "count": Product.objects.filter(price__gte=500).count(),
                }
            )
    else:
        price_ranges = [
            {"name": "Under $100", "min": 0, "max": 99.99, "count": 0},
            {"name": "$100 - $300", "min": 100, "max": 299.99, "count": 0},
            {"name": "$300 - $500", "min": 300, "max": 499.99, "count": 0},
            {"name": "Over $500", "min": 500, "max": None, "count": 0},
        ]

    return Response(
        {
            "brands": list(brands),
            "connections": list(connections),
            "types": [],
            "price_ranges": price_ranges,
        }
    )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def upload_product_image(request, product_id):
    """Upload a product image to ImgBB"""
    try:
        product = get_object_or_404(Product, pk=product_id)
        
        if 'image' not in request.FILES:
            return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['image']
        url = 'https://api.imgbb.com/1/upload'

        payload = {
            'key': settings.IMGBB_API_KEY,
            'name': f"{product.slug}"
        }
        
        files = {
            'image': (image_file.name, image_file.read(), image_file.content_type)
        }
        
        # Make the request
        response = requests.post(url, data=payload, files=files)
        data = response.json()
        
        if not response.ok or not data.get('success'):
            error_msg = data.get('error', {}).get('message', 'Failed to upload image to ImgBB')
            return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)

        image_data = data['data']
        product.image_url = image_data['url']
        product.save()
        return Response({
            'status': 'success',
            'message': 'Image uploaded successfully',
            'image_url': image_data['url'],
        })
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product_image(request, product_id):
    """Delete product image"""
    try:
        product = get_object_or_404(Product, pk=product_id)
        
        if not product.image_url:
            return Response({'error': 'No image to delete'}, status=status.HTTP_400_BAD_REQUEST)
        
        product.image_url = None
        product.image_thumb_url = None
        product.image_delete_url = None
        product.save()
        
        return Response({
            'status': 'success',
            'message': 'Image removed from product'
        })
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)