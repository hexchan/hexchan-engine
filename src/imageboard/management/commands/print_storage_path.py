from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Print absolute path to the storage directory'

    def handle(self, *args, **options):
        return str(settings.STORAGE_DIR)
