from django.db import models


class PaymentItem(models.Model):
    display_name = models.CharField(max_length=100)
    description = models.TextField()
    api_url = models.URLField(max_length=200)

    class Meta:
        app_label = 'ledgerpay'


import reversion
reversion.register(PaymentItem)
