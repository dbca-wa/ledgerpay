from django.db import models


class PaymentItem(models.Model):
    display_name = models.CharField(max_length=100, blank=True)
    api_url = models.URLField(max_length=200, verbose_name='API URL', blank=True)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        app_label = 'ledgerpay'

    def __str__(self):
        return self.display_name


import reversion
reversion.register(PaymentItem)
