from django.contrib.auth.models import AbstractUser

from product_manager import settings


class User(AbstractUser):
    pass

    class Meta:
        app_label = 'products'
        swappable = settings.AUTH_USER_MODEL
