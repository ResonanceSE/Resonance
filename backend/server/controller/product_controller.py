from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from server.models import Product
from server.serializers import ProductSerializer


class initializeController_Product:
    def __str__(self):
        return "Initialize Controller"


# Get all products
@api_view(["GET"])
def get_all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# Get product by name
@api_view(["GET"])
def get_product_by_name(request, name):
    product = get_object_or_404(Product, name__iexact=name)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
