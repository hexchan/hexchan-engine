from django.core.management.base import BaseCommand
from django.conf import settings

CONFIG_TEMPLATE = '''
<VirtualHost {host}:80>
    ServerName {host}

    WSGIDaemonProcess hexchan_engine python-path={install_path}/src python-home={install_path}/python_modules
    WSGIProcessGroup hexchan_engine
    WSGIScriptAlias / {install_path}/src/hexchan/wsgi.py

    <Directory {install_path}/src/hexchan>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    Alias /static {storage_path}/static
    <Directory {storage_path}/static>
        Require all granted
    </Directory>

    Alias /media {storage_path}/upload
    <Directory {storage_path}/upload>
        Require all granted
    </Directory>

    LimitRequestBody 10485760

    ErrorLog ${{APACHE_LOG_DIR}}/error.log
    CustomLog ${{APACHE_LOG_DIR}}/access.log combined
</VirtualHost>
'''.strip()


class Command(BaseCommand):
    help = 'Create Apache 2 host config from values in `settings.py`'

    def handle(self, *args, **options):
        config_text = CONFIG_TEMPLATE.format(
            host=settings.HOST,
            install_path=settings.INSTALL_DIR,
            storage_path=settings.STORAGE_DIR,
        )

        return config_text
