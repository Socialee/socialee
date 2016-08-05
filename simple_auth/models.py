"""
Password models for simple_auth
"""

from django.db import models


class Password(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name
