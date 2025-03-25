import uuid
from django.db import models
from django.conf import settings


class Token(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tokens")
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
