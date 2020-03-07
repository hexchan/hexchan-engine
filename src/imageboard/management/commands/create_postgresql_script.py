from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


SCRIPT_TEMPLATE = '''
create database {name};
create user {user} with password '{password}';
alter role {user} set client_encoding to 'utf8';
alter role {user} set default_transaction_isolation to 'read committed';
alter role {user} set timezone to 'utc';
alter USER {user} CREATEDB;
grant all privileges on database {name} to {user};
'''.strip()


class Command(BaseCommand):
    help = 'Create PostgreSQL database initialization script from values in `settings.py`'

    def handle(self, *args, **options):
        try:
            database_settings = settings.DATABASES['default']
        except (ValueError, KeyError):
            raise CommandError('Variable `DATABASES` or it\'s key `default` not found. Check `settings.py`')

        database_engine = database_settings['ENGINE']

        if not database_engine:
            raise CommandError('`ENGINE` parameter is missing')

        if database_engine != 'django.db.backends.postgresql_psycopg2':
            raise CommandError('Specified `ENGINE` is not PostgreSQL')

        required_settings = ['NAME', 'USER', 'PASSWORD']
        for required_setting in required_settings:
            if not database_settings[required_setting]:
                raise CommandError('Database setting is missing: %s' % required_setting)

        script_text = SCRIPT_TEMPLATE.format(
            name=database_settings['NAME'],
            user=database_settings['USER'],
            password=database_settings['PASSWORD'],
        )

        return script_text
