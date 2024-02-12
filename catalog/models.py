from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    title = models.TextField(max_length=250, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    title = models.TextField(max_length=250, verbose_name='Описание')
    preview = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Изображение')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price_for_one = models.IntegerField(verbose_name='Цена за штуку')
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_last_modified = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Владелец')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    @property
    def active_version(self):
        return self.version_set.filter(is_current=True).first()

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            (
                'set_published',
                'Can publish product'
            )
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    No_version = models.CharField(max_length=50, verbose_name='Номер версии', unique=True)
    name_version = models.CharField(max_length=100, verbose_name='Название версии')
    is_current = models.BooleanField(default=False, verbose_name='Признак текущей версии')

    def __str__(self):
        return f"{self.product.name} - {self.name_version}"

    def save(self, *args, **kwargs):
        if self.is_current:
            # Установка текущей версии только для одной версии продукта
            Version.objects.filter(product=self.product).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'


class Blog(models.Model):
    name = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.CharField(max_length=200, verbose_name='slug', null=True, blank=True)
    content = models.TextField(max_length=500, verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/', null=True, blank=True, verbose_name='Изображение')
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
