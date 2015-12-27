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
