from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class PlatformUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name


class ProductSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} selected {self.product.name} at {self.selected_at}'
