import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Quote(models.Model):
    title = models.TextField(max_length=250, verbose_name='Zitat')
    author = models.CharField(max_length=120, verbose_name='Autor')
    subm_date = models.DateTimeField(null= True, auto_now=True, verbose_name='Datum')
    active = models.BooleanField(default=False, verbose_name='veröffentlicht?')

    class Meta:
        verbose_name = 'Zitat'
        verbose_name_plural = 'Zitate'

    def was_submitted_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(hours=24) <= self.subm_date <= now
    was_submitted_recently.admin_order_field = 'subm_date'
    was_submitted_recently.boolean = True
    was_submitted_recently.short_description = 'Neu?'

    def __str__(self):
        return format(self.title)