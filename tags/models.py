from django.db import models

# Create your models here.
from django.utils.text import slugify

from shared.models import TimestampedModel


class TagManager(models.Manager):

    def get_random_tag(self):
        return Tag.objects.order_by('?').first()

    def get_random_tag_id(self):
        tag = Tag.objects.order_by('?').only('id').first()
        if tag is not None:
            return tag.id
        return None


class Tag(TimestampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)
    description = models.CharField(max_length=140)

    objects = TagManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
