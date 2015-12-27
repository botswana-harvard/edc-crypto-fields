from .base_encrypted_field import BaseEncryptedField


class RestrictedRsaEncryptionField(BaseEncryptedField):

    """   private key is NOT expected to be available and it's absence is enforced """
    def __init__(self, *args, **kwargs):

        # check for settings attribute
        # if 'IS_SECURE_DEVICE' not in dir(settings):
        #      raise ImproperlyConfigured(
        #          'edc_crypto_fields requires boolean settings attribute IS_SECURE_DEVICE. '
        #          'Please add to your django settings file')
        # set alg, mode and defaults
        self.algorithm = 'rsa'
        self.mode = 'restricted'
        defaults = {'help_text':
                    kwargs.get('help_text', '') + ' (Encryption: {0} {1})'.format(self.algorithm, self.mode,)}
        kwargs.update(defaults)
        super(RestrictedRsaEncryptionField, self).__init__(*args, **kwargs)
