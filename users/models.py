from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    avatar = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name='Аватар')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона')
    country = models.CharField(max_length=100, verbose_name='Страна')

    # поля для авторизации вместо имени пользователя
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
