import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User


def upload_location(instance, filename):
    location = str("ideas")
    return "%s/%s" % (location, filename)


class Idea(models.Model):
    picture = models.ImageField(upload_to=upload_location, null=True, blank=True, verbose_name='Bild')
    title = models.CharField(max_length=250, verbose_name='Titel', null=True, blank=True)
    description = models.TextField(max_length=1500, verbose_name='Beschreibung', null=True, blank=True)
    author = models.EmailField(max_length=254, verbose_name='Email des Autors', null=True, blank=True)
    subm_date = models.DateTimeField(auto_now=True, verbose_name='Datum', null=True, blank=True)
    active = models.BooleanField(default=False, verbose_name='veröffentlicht?')
    money = models.ManyToManyField(User, related_name='gives_money_to')
    hands = models.ManyToManyField(User, related_name='gives_hand_to')
    likes = models.ManyToManyField(User, related_name='likes_ideas')

    class Meta:
        verbose_name = 'Idee'
        verbose_name_plural = 'Ideen'

    def was_submitted_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(hours=24) <= self.subm_date <= now
    was_submitted_recently.admin_order_field = 'subm_date'
    was_submitted_recently.boolean = True
    was_submitted_recently.short_description = 'Neu?'

    def __str__(self):
        return format(self.title)