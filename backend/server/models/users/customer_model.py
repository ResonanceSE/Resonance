from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    """Extend Django's default user model if needed"""
    
    # Avoid conflicts with Django's default auth.User
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Change this name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Change this name
        blank=True
    )

    def __str__(self):
        return self.username
