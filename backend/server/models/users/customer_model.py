from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    """Extend Django's default user model if needed"""

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True,
    )

    def __str__(self):
        return self.username
