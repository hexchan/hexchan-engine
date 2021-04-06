from django.core.management.base import BaseCommand, CommandError
from django.db import Error as DbError

from imageboard.models.captcha import Captcha
from imageboard.utils.captchamaker import make_captcha_create_kwargs


class Command(BaseCommand):
    help = 'Populate captcha database'
    requires_system_checks = True
    requires_migrations_check = True

    def add_arguments(self, parser):
        parser.add_argument('num')

    def handle(self, *args, **options):
        captchas = []
        num = int(options['num'], 10)
        for i in range(num):
            captcha_kwargs = make_captcha_create_kwargs()
            captchas.append(Captcha(**captcha_kwargs))
        try:
            Captcha.objects.bulk_create(captchas)
        except DbError:
            raise CommandError('Database error occured')
