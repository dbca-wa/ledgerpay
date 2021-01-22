from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class GlobalSettings(models.Model):
    keys = ((),)
    default_values = ((),)

    key = models.CharField(max_length=255, choices=keys, blank=False, null=False, unique=True)
    value = models.CharField(max_length=255)

    class Meta:
        app_label = 'ledgerpay'
        verbose_name_plural = "Global Settings"


@python_2_unicode_compatible
class SystemMaintenance(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def duration(self):
        """ Duration of system maintenance (in mins) """
        return int( (self.end_date - self.start_date).total_seconds()/60.) if self.end_date and self.start_date else ''
    duration.short_description = 'Duration (mins)'

    class Meta:
        app_label = 'ledgerpay'
        verbose_name_plural = "System maintenance"

    def __str__(self):
        return 'System Maintenance: {} ({}) - starting {}, ending {}'.format(self.name, self.description, self.start_date, self.end_date)


import reversion
reversion.register(GlobalSettings)
reversion.register(SystemMaintenance)
