from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class Customer(AbstractUser):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    # Shipping address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
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
