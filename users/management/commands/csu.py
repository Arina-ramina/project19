from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='arinafedor23@icloud.com',
            first_name='Admin',
            last_name='Arina',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('2310')
        user.save()
