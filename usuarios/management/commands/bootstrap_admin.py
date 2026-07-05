import os
import secrets
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea el primer usuario administrador de forma idempotente'

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('Admin ya existe — saltando bootstrap')
            return

        env = os.getenv('ENV', 'dev')

        if env == 'prod':
            password = secrets.token_urlsafe(32)
            self.stderr.write(self.style.WARNING(
                'ADMIN_BOOTSTRAP_PASSWORD ignorada en entorno de producción — generando password aleatoria'
            ))
        else:
            password = os.getenv('ADMIN_BOOTSTRAP_PASSWORD') or secrets.token_urlsafe(24)

        User.objects.create_superuser(
            username='admin',
            email='admin@telepark.com',
            password=password,
            first_name='Admin',
            last_name='Sistema',
            is_active=True,
        )

        self.stdout.write(self.style.SUCCESS(f'Admin creado exitosamente. Username: admin'))

        if env != 'prod' and not os.getenv('ADMIN_BOOTSTRAP_PASSWORD'):
            self.stdout.write(f'Password generada: {password}')
