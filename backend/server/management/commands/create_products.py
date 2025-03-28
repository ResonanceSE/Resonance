from django.core.management.base import BaseCommand
from django.utils.text import slugify
from server.models import Product, Category
from decimal import Decimal


class Command(BaseCommand):
    help = "Create initial products"

    def handle(self, *args, **kwargs):
        # Get categories
        try:
            headphones = Category.objects.get(slug="headphones")
            speakers = Category.objects.get(slug="speakers")
            earbuds = Category.objects.get(slug="earbuds")
        except Category.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f"Category not found: {str(e)}"))
            return

        products = [
            {
                "name": "Sony WH-1000XM4",
                "description": "Industry-leading noise canceling with Dual Noise Sensor technology",
                "category": headphones,
                "brand": "Sony",
                "connections": "Bluetooth 5.0, 3.5mm",
                "price": Decimal("349.99"),
                "stock": 50,
                "is_featured": True,
                "image_url": "https://example.com/sony-wh1000xm4.jpg",
            },
            {
                "name": "Bose SoundLink Revolve+",
                "description": "360-degree coverage for consistent, uniform coverage",
                "category": speakers,
                "brand": "Bose",
                "connections": "Bluetooth, 3.5mm",
                "price": Decimal("299.99"),
                "stock": 30,
                "is_featured": True,
                "image_url": "https://example.com/bose-revolve-plus.jpg",
            },
            {
                "name": "Apple AirPods Pro",
                "description": "Active Noise Cancellation for immersive sound",
                "category": earbuds,
                "brand": "Apple",
                "connections": "Bluetooth 5.0",
                "price": Decimal("249.99"),
                "stock": 100,
                "is_featured": True,
                "image_url": "https://example.com/airpods-pro.jpg",
            },
        ]

        for product_data in products:
            try:
                product_data["slug"] = slugify(product_data["name"])
                product, created = Product.objects.get_or_create(**product_data)
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Created product: {product_data['name']}")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Product already exists: {product_data['name']}"
                        )
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error creating product {product_data['name']}: {str(e)}"
                    )
                )
