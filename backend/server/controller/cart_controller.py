from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Cart, CartItem, Product


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    """Get the user's cart with all items"""
    user = request.user
    
    # Get or create the user's cart
    cart, _ = Cart.objects.get_or_create(user=user)
    
    # Get all cart items with their product information
    cart_items = []
    for item in cart.items.all():
        cart_items.append({
            "id": item.id,
            "product_id": item.product.id,
            "name": item.product.name,
            "price": float(item.product.sale_price or item.product.price),
            "quantity": item.quantity,
            "image_url": item.product.image_url,
            "category": item.product.category.name if item.product.category else None,
            "stock": item.product.stock,
        })
    
    return Response({
        "status": "success",
        "data": cart_items
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """Add a product to the user's cart or update quantity if already exists"""
    user = request.user
    data = request.data
    
    # Validate input
    if not data.get("product_id"):
        return Response({
            "status": "error",
            "message": "Product ID is required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    quantity = int(data.get("quantity", 1))
    if quantity <= 0:
        return Response({
            "status": "error",
            "message": "Quantity must be greater than 0"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        product = get_object_or_404(Product, id=data["product_id"])
        
        # Check if product is in stock
        if product.stock < quantity:
            return Response({
                "status": "error",
                "message": f"Not enough stock. Only {product.stock} available."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create user's cart
        cart, _ = Cart.objects.get_or_create(user=user)
        
        # Check if product already in cart
        cart_item = cart.items.filter(product=product).first()
        
        if cart_item:
            # If adding more would exceed stock, return error
            if cart_item.quantity + quantity > product.stock:
                return Response({
                    "status": "error",
                    "message": f"Cannot add more items. You already have {cart_item.quantity} in your cart, and only {product.stock} are available."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update existing cart item
            cart_item.quantity += quantity
            cart_item.save()
            item_id = cart_item.id
        else:
            # Create new cart item
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )
            item_id = cart_item.id
        
        return Response({
            "status": "success",
            "message": "Item added to cart",
            "data": {
                "id": item_id,
                "product_id": product.id,
                "name": product.name,
                "price": float(product.sale_price or product.price),
                "quantity": cart_item.quantity,
                "image_url": product.image_url,
                "category": product.category.name if product.category else None,
                "stock": product.stock,
            }
        })
        
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    """Update the quantity of a cart item"""
    user = request.user
    data = request.data
    
    # Validate input
    if "quantity" not in data:
        return Response({
            "status": "error",
            "message": "Quantity is required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    quantity = int(data["quantity"])
    if quantity <= 0:
        return Response({
            "status": "error",
            "message": "Quantity must be greater than 0"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Ensure cart item belongs to user
        cart = Cart.objects.get(user=user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        # Check stock
        if quantity > cart_item.product.stock:
            return Response({
                "status": "error",
                "message": f"Not enough stock. Only {cart_item.product.stock} available."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update quantity
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response({
            "status": "success",
            "message": "Cart item updated",
            "data": {
                "id": cart_item.id,
                "product_id": cart_item.product.id,
                "quantity": cart_item.quantity
            }
        })
        
    except Cart.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Cart not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except CartItem.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Cart item not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    """Remove an item from the cart"""
    user = request.user
    
    try:
        # Ensure cart item belongs to user
        cart = Cart.objects.get(user=user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        # Delete cart item
        cart_item.delete()
        
        return Response({
            "status": "success",
            "message": "Item removed from cart"
        })
        
    except Cart.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Cart not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except CartItem.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Cart item not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """Remove all items from the user's cart"""
    user = request.user
    
    try:
        # Get user's cart
        cart = Cart.objects.get(user=user)
        
        # Delete all items in the cart
        cart.items.all().delete()
        
        return Response({
            "status": "success",
            "message": "Cart cleared"
        })
        
    except Cart.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Cart not found"
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sync_cart(request):
    """
    Synchronize the cart between devices:
    Takes client-side cart items and merges them with server-side cart
    """
    user = request.user
    data = request.data
    
    # Validate input
    if not data.get("items") or not isinstance(data.get("items"), list):
        return Response({
            "status": "error",
            "message": "Cart items array is required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            # Get or create user's cart
            cart, _ = Cart.objects.get_or_create(user=user)
            
            # Store items to add to cart
            items_to_add = []
            for item_data in data["items"]:
                product_id = item_data.get("id") or item_data.get("product_id")
                quantity = item_data.get("quantity", 1)
                
                if not product_id or not quantity:
                    continue
                    
                try:
                    product = Product.objects.get(id=product_id)
                    
                    # Check if this product is already in the server cart
                    existing_item = cart.items.filter(product=product).first()
                    
                    if existing_item:
                        # Merge quantities, but don't exceed stock
                        new_quantity = min(existing_item.quantity + quantity, product.stock)
                        existing_item.quantity = new_quantity
                        existing_item.save()
                    else:
                        # Add new cart item with quantity limited by stock
                        new_quantity = min(quantity, product.stock)
                        items_to_add.append(CartItem(
                            cart=cart,
                            product=product,
                            quantity=new_quantity
                        ))
                except Product.DoesNotExist:
                    continue
            
            # Bulk create any new items
            if items_to_add:
                CartItem.objects.bulk_create(items_to_add)
            
            # Get updated cart data
            updated_items = []
            for item in cart.items.all():
                updated_items.append({
                    "id": item.id,
                    "product_id": item.product.id,
                    "name": item.product.name,
                    "price": float(item.product.sale_price or item.product.price),
                    "quantity": item.quantity,
                    "image_url": item.product.image_url,
                    "category": item.product.category.name if item.product.category else None,
                    "stock": item.product.stock,
                })
            
            return Response({
                "status": "success",
                "message": "Cart synchronized successfully",
                "data": updated_items
            })
            
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)