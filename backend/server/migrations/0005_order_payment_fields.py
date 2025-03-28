# Generated by Django 5.1.4 on 2025-03-29 12:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("server", "0002_remove_product_dimensions_remove_product_sku"),
        ("server", "0004_user_reset_token_user_reset_token_expiry_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payment_method",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("processing", "Processing"),
                    ("shipped", "Shipped"),
                    ("delivered", "Delivered"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
