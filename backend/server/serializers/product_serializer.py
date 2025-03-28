from rest_framework import serializers
from django.utils.text import slugify
from server.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("slug", "created_at", "updated_at")

    def create(self, validated_data):
        # Generate a unique slug from the name
        name = validated_data.get("name")
        base_slug = slugify(name)
        slug = base_slug
        counter = 1

        # Ensure slug uniqueness
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        validated_data["slug"] = slug

        return super().create(validated_data)

    def validate(self, data):
        # Validate sale price is less than regular price
        if "sale_price" in data and data["sale_price"]:
            if data["sale_price"] >= data.get("price", 0):
                raise serializers.ValidationError(
                    {"sale_price": "Sale price must be less than regular price"}
                )

        # Validate price is positive
        if "price" in data and data["price"] <= 0:
            raise serializers.ValidationError(
                {"price": "Price must be greater than zero"}
            )

        # Validate stock is non-negative
        if "stock" in data and data["stock"] < 0:
            raise serializers.ValidationError({"stock": "Stock cannot be negative"})

        return data
