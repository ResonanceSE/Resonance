from django.db import models
from django.contrib.auth.models import User
import uuid

import random
import string
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens")
    key = models.CharField(max_length=64, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return uuid.uuid4().hex

    class Meta:
        db_table = "auth_token"
