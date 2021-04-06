import os
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from imageboard.utils.captchamaker import make_captcha_create_kwargs


class Command(BaseCommand):
    help = 'Generate captcha fixtures'
    requires_system_checks = True
    requires_migrations_check = True

    def add_arguments(self, parser):
        parser.add_argument('num')

    def handle(self, *args, **options):
        fixtures = []
        num = int(options['num'], 10)
        for i in range(1, num + 1):
            captcha_kwargs = make_captcha_create_kwargs()
            captcha_fixture = {
                "model": "imageboard.captcha",
                "pk": i,
                "fields": captcha_kwargs,
            }
            fixtures.append(captcha_fixture)

        fixture_filename = os.path.join(settings.FIXTURE_DIRS[0], 'captchas.json')
        with open(fixture_filename, 'w') as captcha_file:
            json.dump(fixtures, captcha_file, indent=4, ensure_ascii=False)
