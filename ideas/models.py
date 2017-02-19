import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


def upload_location(instance, filename):
    title = str(instance.title)
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d_%HUhr%M")
    return "%s/%s/%s/%s" % (str("ideas"), title, date, filename)


class Idea(models.Model):
    picture = models.ImageField(upload_to=upload_location, null=True, blank=True, verbose_name='Bild')
    title = models.CharField(max_length=250, verbose_name='Titel', null=True, blank=True)
    description = models.TextField(max_length=1500, verbose_name='Beschreibung', null=True, blank=True)
    author = models.EmailField(max_length=254, verbose_name='Email des Autors', null=True, blank=True)
    authorUser = models.ForeignKey(User, null=True, blank=True)
    subm_date = models.DateTimeField(auto_now_add=True, verbose_name='Datum', null=True, blank=True)
    featured = models.BooleanField(default=False, verbose_name='featured')
    private = models.BooleanField(default=False, verbose_name='Privat ')
    enabled = models.BooleanField(default=False, verbose_name='Freigegeben')
    active = models.BooleanField(default=True, verbose_name='Ohne Projekt')
    likes = models.ManyToManyField(User, related_name='likes_ideas')
    project = models.OneToOneField('socialee.Project', null=True, blank=True)

    class Meta:
        verbose_name = 'Idee'
        verbose_name_plural = 'Ideen'


    def was_submitted_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(hours=24) <= self.subm_date <= now
    was_submitted_recently.admin_order_field = 'subm_date'
    was_submitted_recently.boolean = True
    was_submitted_recently.short_description = 'Neu'


    def thumb(self):
        if self.picture:
            return mark_safe(u'<img src="%s" width=60 height=60 />' % (self.picture.url))
        else:
            return u''

    thumb.short_description = 'Vorschau'

    # def has_delete_permission(self, request, obj=None):
    #     if obj and obj.private and hasattr(request.user, 'email') and request.user.email != obj.author:
    #         print("inhere")
    #         return False
    #     print("nope")
    #     return super(Idea, self).has_delete_permission(request, obj)

    def __str__(self):
        return format(self.title)

class Comment(models.Model):
    to_idea = models.ForeignKey(Idea, null=True, blank=True, related_name='comments')
    by_user = models.ForeignKey(User, null=True, blank=True)
    message = models.TextField(max_length=140, null=True, blank=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    class Meta:
        ordering = ['-date']