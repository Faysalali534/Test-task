from django.contrib.auth.models import AbstractUser

from product_manager import settings
from django.db import models


class User(AbstractUser):
    pass

    class Meta:
        app_label = 'products'
        swappable = settings.AUTH_USER_MODEL


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    selected = models.BooleanField(default=False)

    def __str__(self):
        return self.name
