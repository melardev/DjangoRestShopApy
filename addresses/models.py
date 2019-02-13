# Create your models here.
from django.db import models

from shared.models import TimestampedModel
from users.models import AppUser


class Address(TimestampedModel):
    user = models.ForeignKey(
        # settings.AUTH_USER_MODEL, # better practice, but no intellisense in filter(), exclude , etc.
        AppUser,  # intellisense available, at least in pycharm :)
        related_name='addresses', null=True, blank=True, on_delete=models.SET_NULL,
        verbose_name='User')

    first_name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=50)
    country = models.CharField(blank=False, max_length=50)
    city = models.CharField(blank=False, max_length=50)
    address = models.CharField(blank=False, max_length=50)
    zip_code = models.CharField(blank=False, max_length=20)
