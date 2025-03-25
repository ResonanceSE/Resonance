from django.core.management.base import BaseCommand
from django.utils.text import slugify
from server.models import Category

class Command(BaseCommand):
    help = 'Create initial categories'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Headphones',
                'description': 'High-quality headphones for immersive audio experience',
            },
            {
                'name': 'Speakers',
                'description': 'Powerful speakers for room-filling sound',
            },
            {
                'name': 'Earbuds',
                'description': 'Compact and portable earbuds for on-the-go listening',
            },
            {
                'name': 'Accessories',
                'description': 'Essential accessories for your audio equipment',
            },
            {
                'name': 'Microphones',
                'description': 'Professional microphones for recording and streaming',
            },
        ]

        for category_data in categories:
            category_data['slug'] = slugify(category_data['name'])
            Category.objects.get_or_create(**category_data)
            self.stdout.write(self.style.SUCCESS(f'Created category: {category_data["name"]}')) 