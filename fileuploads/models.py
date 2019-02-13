from django.db import models
# Create your models here.
from polymorphic.models import PolymorphicModel

from categories.models import Category
from products.models import Product
from tags.models import Tag
from users.models import AppUser


# https://django-polymorphic.readthedocs.io/en/stable/quickstart.html#making-your-models-polymorphic
class FileUpload(PolymorphicModel):
    file_name = models.CharField(max_length=120)
    file_path = models.CharField(max_length=250)
    original_name = models.CharField(max_length=120)
    file_length = models.IntegerField()


class TagImage(FileUpload):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='images')


class ProductImage(FileUpload):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class CategoryImage(FileUpload):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='images')


class ProfileImage(FileUpload):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='avatars')
