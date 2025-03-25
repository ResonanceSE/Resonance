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
            accessories = Category.objects.get(slug="accessories")
            microphones = Category.objects.get(slug="microphones")
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
                "sku": "SONY-WH1000XM4",
                "weight": Decimal("0.25"),
                "dimensions": "7.3 x 3.0 x 9.9 inches",
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
                "sku": "BOSE-REVOLVEPLUS",
                "weight": Decimal("0.9"),
                "dimensions": "4.13 x 4.13 x 7.25 inches",
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
                "sku": "APPLE-AIRPODSPRO",
                "weight": Decimal("0.05"),
                "dimensions": "1.22 x 0.86 x 0.94 inches",
                "is_featured": True,
                "image_url": "https://example.com/airpods-pro.jpg",
            },
            {
                "name": "Audio-Technica ATH-M50x",
                "description": "Professional studio monitor headphones",
                "category": headphones,
                "brand": "Audio-Technica",
                "connections": "3.5mm, 6.3mm",
                "price": Decimal("149.99"),
                "stock": 75,
                "sku": "AT-M50X",
                "weight": Decimal("0.28"),
                "dimensions": "11.4 x 10 x 4.1 inches",
                "is_featured": False,
                "image_url": "https://example.com/ath-m50x.jpg",
            },
            {
                "name": "Blue Yeti USB Microphone",
                "description": "Professional USB microphone for streaming and recording",
                "category": microphones,
                "brand": "Blue",
                "connections": "USB",
                "price": Decimal("129.99"),
                "stock": 40,
                "sku": "BLUE-YETI",
                "weight": Decimal("1.2"),
                "dimensions": "4.72 x 4.92 x 11.61 inches",
                "is_featured": True,
                "image_url": "https://example.com/blue-yeti.jpg",
            },
            {
                "name": "Headphone Stand",
                "description": "Universal aluminum headphone stand",
                "category": accessories,
                "brand": "Generic",
                "connections": "N/A",
                "price": Decimal("24.99"),
                "stock": 200,
                "sku": "ACC-HPSTAND",
                "weight": Decimal("0.5"),
                "dimensions": "4.5 x 4.5 x 10.2 inches",
                "is_featured": False,
                "image_url": "https://example.com/headphone-stand.jpg",
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
