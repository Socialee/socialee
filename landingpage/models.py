from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

def upload_location(instance, filename):
    location = str("landingpage")
    return "%s/%s" % (location, filename)

class Landingpage(models.Model):
    bg_img = models.ImageField(upload_to=upload_location)
    symbol = models.FileField(upload_to=upload_location)
    claim = models.CharField(max_length=250)
    tagline = models.TextField(max_length=500)
    cta = RichTextField()
    active = models.BooleanField(default=False, verbose_name='veröffentlicht?')

    def __str__(self):
        return self.claim