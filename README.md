[![Build Status](https://travis-ci.org/botswana-harvard/edc-crypto-fields.svg?branch=develop)](https://travis-ci.org/botswana-harvard/edc-crypto-fields) [![Coverage Status](https://coveralls.io/repos/botswana-harvard/edc-crypto-fields/badge.svg?branch=develop&service=github)](https://coveralls.io/github/botswana-harvard/edc-crypto-fields?branch=develop)

# edc-crypto-fields
Encrypt model fields -- like django-crypto-fields but uses M2Crypto

This is the original version written under Django 1.6 and PY2. Newer projects will use `django-crypto-fields` as M2Crypto does not seem to have PY3 support.

For the Edc projects, these classes are imported via `edc_base.encrypted_fields`.

In settings:

    INSTALLED_APPS = (
    ...
    'edc_crypto_fields',
    ...
    )
    
and add the KEY_PATH:

    KEY_PATH = '<my folder with keys>'
    
After settings has been updates, keys can be generated using a management command:

    python manage.py generate_keys
    
The keys will be generated and placed in the folder specified in `KEY_PATH`. This is where the project will look for keys whenever it needs to encrypt a field.


If using synchronization (`edc_sync.SyncModelMixin`), you can specifiy the default `using` attribute for the `Crypt` model. In most cases a client's database key will be 'default' and the server be 'server'. This is OK as the client does not attempt deserialization. See tests in `edc_sync`.

    EDC_CRYPTO_FIELDS_CLIENT_USING = 'client'  # defaults to 'default' if not specified
