from django.core.management.base import BaseCommand
from server.models import Customer
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Create initial superuser for admin access"

    def handle(self, *args, **kwargs):
        try:
            admin_data = {
                "username": "Than",
                "email": "kuy.siriphiwat@gmail.com",
                "password": "than1234",
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            }

            # Check if user already exists
            if Customer.objects.filter(username=admin_data["username"]).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"Superuser with username '{admin_data['username']}' already exists"
                    )
                )
                return

            # Create superuser
            user = Customer.objects.create_superuser(
                username=admin_data["username"],
                email=admin_data["email"],
                password=admin_data["password"],
                first_name=admin_data["first_name"],
                last_name=admin_data["last_name"],
            )
            print(user)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superuser '{admin_data['username']}' created successfully"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Login with username: {admin_data['username']}, password: {admin_data['password']}"
                )
            )

        except IntegrityError:
            self.stdout.write(
                self.style.ERROR(
                    f"Superuser with username '{admin_data['username']}' or email '{admin_data['email']}' already exists"
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating superuser: {str(e)}"))
