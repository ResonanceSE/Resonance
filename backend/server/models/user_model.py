from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False, is_superuser=False)

    def get_active_customers(self):
        return self.get_queryset().filter(is_active=True)

    def with_recent_orders(self, days=30):
        from django.utils import timezone
        from datetime import timedelta

        recent_date = timezone.now() - timedelta(days=days)
        return (
            self.get_queryset().filter(orders__created_at__gte=recent_date).distinct()
        )


class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)


class User(AbstractUser):
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Password reset
    reset_token = models.CharField(max_length=64, null=True, blank=True)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.username

    def get_full_address(self):
        parts = [self.address, self.city, self.state, self.postal_code, self.country]
        return ", ".join(filter(None, parts))

    def has_active_orders(self):
        return self.orders.filter(status__in=["pending", "processing"]).exists()

    def get_cart_total(self):
        if hasattr(self, "cart"):
            return sum(
                item.product.current_price * item.quantity
                for item in self.cart.items.all()
            )
        return 0


class Customer(User):
    """
    Proxy model for regular customers (non-admin users)
    """

    objects = CustomerManager()

    class Meta:
        proxy = True
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def get_order_count(self):
        return self.orders.count()

    def get_total_spent(self):
        from django.db.models import Sum

        return (
            self.orders.filter(status="delivered").aggregate(total=Sum("total_amount"))[
                "total"
            ]
            or 0
        )

    def get_wishlist(self):
        # Example method - would need a wishlist model
        if hasattr(self, "wishlist"):
            return self.wishlist.products.all()
        return []

    def get_recent_orders(self, limit=5):
        return self.orders.all().order_by("-created_at")[:limit]


class AdminStaff(User):
    """
    Proxy model for admin users
    """

    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"

    def get_managed_orders(self):
        from ..models import Order

        return Order.objects.all()

    def get_admin_stats(self):
        from ..models import Order, Product

        stats = {
            "total_customers": Customer.objects.count(),
            "total_products": Product.objects.count(),
            "low_stock_products": Product.objects.filter(stock__lt=10).count(),
            "pending_orders": Order.objects.filter(status="pending").count(),
        }
        return stats

    def can_manage_products(self):
        return self.is_superuser or self.groups.filter(name="Product Managers").exists()

    def can_manage_orders(self):
        return self.is_superuser or self.groups.filter(name="Order Managers").exists()
