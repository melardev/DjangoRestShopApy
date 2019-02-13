from django.db import models

# Create your models here.
from products.models import Product
from shared.models import TimestampedModel
from users.models import AppUser


class Comment(TimestampedModel):
    content = models.TextField()
    rating = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey(Product, related_name='comments', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        # settings.AUTH_USER_MODEL,
        AppUser,
        related_name='comments', on_delete=models.CASCADE
    )
