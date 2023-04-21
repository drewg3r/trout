from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Assures there is a superuser with parameters as specified. " \
           "If the user already exists, its properties are updated"

    def add_arguments(self, parser):

        parser.add_argument('--username', help="username of the new/updated admin, required", required=True)
        parser.add_argument('--password', help="password of the new/updated admin, required", required=True)

    def handle(self, *args, **options):
        user, created = get_user_model().objects.update_or_create(
            username=options['username'],
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(options['password'])
        user.save()
