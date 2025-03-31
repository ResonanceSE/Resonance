from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False, is_superuser=False)

    def get_active_customers(self):
        return self.get_queryset().filter(is_active=True)

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


class Customer(User):
    """
    Proxy model for regular customers (non-admin users)
    """

    objects = CustomerManager()

    class Meta:
        proxy = True
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class AdminStaff(User):
    """
    Proxy model for admin users
    """

    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"



