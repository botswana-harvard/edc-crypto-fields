from django.conf import settings
from django.core.management.base import BaseCommand

from edc.core.crypto_fields.utils import setup_new_keys


class Command(BaseCommand):
    help = 'Generate new encryption keys.'

    def handle(self, *args, **options):
        try:
            key_path = args[0]
        except IndexError:
            key_path = settings.KEY_PATH
        setup_new_keys(key_path)
