from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin

# try:
#     from edc.device.dispatch.models import BaseDispatchSyncUuidModel
#
#     class BaseCrypt(BaseDispatchSyncUuidModel):
#         class Meta:
#             abstract = True
#
# except ImportError:
#
#     class BaseCrypt(models.Model):
#         class Meta:
#             abstract = True


class CryptoManager(models.Manager):

    def get_by_natural_key(self, hash_value, algorithm, mode):
        return self.get(hash=hash_value, algorithm=algorithm, mode=mode)


class Crypt(SyncModelMixin, BaseUuidModel):

    """ A secrets lookup model searchable by hash """

    hash = models.CharField(
        verbose_name="Hash",
        max_length=128,
        db_index=True,
        unique=True)

    secret = models.TextField(
        verbose_name="Secret")

    algorithm = models.CharField(
        max_length=25,
        db_index=True,
        null=True)

    mode = models.CharField(
        max_length=25,
        db_index=True,
        null=True)

    salt = models.CharField(
        max_length=50,
        null=True)

    objects = CryptoManager()

    def natural_key(self):
        return (self.hash, self.algorithm, self.mode,)

    class Meta:
        app_label = 'edc_crypto_fields'
        db_table = 'crypto_crypt'
        verbose_name = 'Crypt'
        unique_together = (('hash', 'algorithm', 'mode'),)
