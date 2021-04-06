from django.core.management.base import BaseCommand

from imageboard.utils.captchamaker import draw_test_sheet


class Command(BaseCommand):
    help = 'Show captcha test sheet'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        draw_test_sheet()
