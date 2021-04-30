from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Create directory structure inside the storage directory'

    def handle(self, *args, **options):
        storage_path = settings.STORAGE_DIR

        directory_paths = [
            storage_path,
            storage_path / 'upload',
            storage_path / 'upload' / 'images',
            storage_path / 'upload' / 'thumbs',
            storage_path / 'session',
            storage_path / 'cache',
            storage_path / 'static',
            storage_path / 'fixtures',
        ]

        try:
            for directory_path in directory_paths:
                directory_path.mkdir(parents=True)
        except PermissionError:
            raise CommandError('Filesystem permission denied')
        except FileExistsError:
            raise CommandError('Directory %s already exists' % directory_path)
        except OSError:
            raise CommandError('Failed to create storage directories')
