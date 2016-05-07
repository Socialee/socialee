from django.db import models

# Create your models here.

class Quote(models.Model):
    title = models.TextField(max_length=1000)
    author = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return format(self.title)