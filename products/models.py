import datetime

from django.core.validators import MinValueValidator
from django.db import models
# Create your models here.
from django.utils.text import slugify

from categories.models import Category
from shared.models import TimestampedModel
from tags.models import Tag


class Product(TimestampedModel):
    name = models.CharField(blank=False, null=False, max_length=200)
    slug = models.CharField(blank=False, null=False, max_length=100)
    description = models.TextField(blank=False, null=False)
    price = models.FloatField(validators=[MinValueValidator(0.1)])
    publish_on = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(
        Tag, related_name='products'
    )

    categories = models.ManyToManyField(
        Category, related_name='products'
    )
    stock = models.IntegerField(validators=[MinValueValidator(0)])

    def save(self, slug="", *args, **kwargs):
        if not self.publish_on:
            self.publish_on = datetime.datetime.now()
            # self.slug = unique_slug(self.title)
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)
