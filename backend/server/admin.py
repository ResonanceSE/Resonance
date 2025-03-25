from django.contrib import admin
from .models.product_model import Product
from .models.customer_model import Customer
from .models.ecommerce_model import (
    Category,
    Order,
    OrderItem,
    Cart,
    CartItem,
    Review,
    Wishlist,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "created_at")
    list_filter = ("parent", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "brand",
        "price",
        "sale_price",
        "stock",
        "is_active",
        "is_featured",
    )
    list_filter = (
        "category",
        "brand",
        "is_active",
        "is_featured",
        "is_new",
        "created_at",
    )
    search_fields = ("name", "description", "sku")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created_at",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "phone_number",
        "is_active",
        "is_email_verified",
        "created_at",
    )
    list_filter = (
        "is_active",
        "is_email_verified",
        "newsletter_subscription",
        "created_at",
    )
    search_fields = ("username", "email", "phone_number", "address")
    ordering = ("-date_joined",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "status",
        "total_amount",
        "payment_status",
        "created_at",
    )
    list_filter = ("status", "payment_status", "created_at")
    search_fields = ("order_number", "user__username", "user__email")
    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "created_at")
    list_filter = ("created_at",)
    search_fields = ("order__order_number", "product__name")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__username", "user__email")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "created_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("cart__user__username", "product__name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__name", "user__username", "comment")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__username", "products__name")
