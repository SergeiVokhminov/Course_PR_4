from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email="admin@mail.ru", first_name="Админ")
        user.set_password("0admin0")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully created admin user with email {user.email}'))
