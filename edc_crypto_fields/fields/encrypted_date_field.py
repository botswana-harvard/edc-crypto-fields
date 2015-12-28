import datetime
import json

from django.conf import settings
from django import forms
from django.utils import timezone
from django.db import models
from django.utils import dateparse
from django.core import exceptions
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder

from .local_rsa_encryption_field import LocalRsaEncryptionField


class EncryptedDateField(LocalRsaEncryptionField, models.DateField):
    __metaclass__ = models.SubfieldBase
    form_widget = forms.DateInput
    form_field = forms.DateField
    save_format = "%Y:%m:%d"
    date_class = datetime.date
    max_raw_length = 10  # YYYY:MM:DD

    def to_python(self, value):
        """ Returns the decrypted date IF the private key is found, otherwise returns
               the encrypted value.

        Value comes from DB as a hash (e.g. <hash_prefix><hashed_value>). If DB value is being
        acccessed for the first time, value is not an encrypted value (not a prefix+hashed_value)."""
        to_python = value
        if to_python is None:
            return to_python
        elif isinstance(to_python, datetime.datetime):
            if settings.USE_TZ and timezone.is_aware(value):
                # Convert aware datetimes to the default time zone
                # before casting them to dates (#17742).
                default_timezone = timezone.get_default_timezone()
                to_python = timezone.make_naive(value, default_timezone)
            to_python = to_python.date()
        elif isinstance(to_python, datetime.date):
            pass
        else:
            value = str(value)
            if not self.algorithm or not self.mode:
                raise ValidationError('Algorithm and mode not set for encrypted field')
            # decrypt will check if is_encrypted (e.g. enc1::<hash>)
            to_python = self.decrypt(value)
            to_python = json.loads(to_python)
            try:
                to_python = dateparse.parse_date(to_python)
            except ValueError:
                raise exceptions.ValidationError(self.error_messages['invalid_date'] % to_python)
            if not to_python:
                raise exceptions.ValidationError(self.error_messages['invalid'] % to_python)
        return to_python or value

    def get_prep_value(self, value, encrypt=True):
        """ Returns the hashed_value with prefix (or None) and, if needed, updates the secret lookup.

        Keyword arguments:
        encrypt -- if False, the value is returned as is (default True)

        """
        value = self.to_python(value)
        retval = value
        if value and encrypt:
            value = json.dumps(value, cls=DjangoJSONEncoder)
            encrypted_value = self.encrypt(value)
            retval = self.field_cryptor.get_prep_value(encrypted_value, value)
        return retval
