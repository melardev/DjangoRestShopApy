from django.db import models
# Create your models here.
from django.utils.text import slugify

from shared.models import TimestampedModel


class CategoryManager(models.Manager):

    def gent_random_category(self):
        return Category.objects.order_by('?').first()


class Category(TimestampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)
    description = models.CharField(max_length=140)

    objects = CategoryManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
