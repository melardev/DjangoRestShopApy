from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# Create your models here.


class AppUserManager(UserManager):

    def is_trusty_comment(self):
        pass

    def get_admin(self):
        return UserManager.filter(self, is_superuser=True).first()


class AppUser(AbstractUser):
    objects = AppUserManager()
