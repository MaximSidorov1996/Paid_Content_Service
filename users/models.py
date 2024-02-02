from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='номер телефона')
    is_active = models.BooleanField(default=False, verbose_name='активен')
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone_number)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

