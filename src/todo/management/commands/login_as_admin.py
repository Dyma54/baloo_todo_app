from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from todo.models import Todo

UserModel = get_user_model()

ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = 'admin@gmail.com'
ADMIN_PASSWORD = 'admin@123'

class Command(BaseCommand):
    help = 'Initialisation du projet et connexion en tant que Admin'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        Todo.objects.all().delete()
        UserModel.objects.all().delete()

        UserModel.objects.create_superuser(username=ADMIN_USERNAME, email=ADMIN_EMAIL, password=ADMIN_PASSWORD)
        self.stdout.write(self.style.SUCCESS('Vous êtes désormais admin'))





