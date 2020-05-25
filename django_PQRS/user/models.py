from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from .managers import CustomUserManager
from django.dispatch import receiver
from django.conf import settings
from django.db import models

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique = True)
    name = models.CharField(max_length = 100, blank = True)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    date_joined = models.DateTimeField(auto_now = True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.name

@receiver(post_save, sender = CustomUser)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)