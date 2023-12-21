import json
from django.core.management import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("data.json", "r") as f:
            data = json.load(f)

        # Очистка данных
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Создание категорий
        category_map = {}
        for item in data:
            if item['model'] == 'catalog.category':
                category = Category(**item['fields'])
                category.save()
                category_map[item['pk']] = category

        # Создание продуктов
        products = []
        for item in data:
            if item['model'] == 'catalog.product':
                product_data = item['fields']
                product_data['category'] = category_map[product_data['category']]
                products.append(Product(**product_data))

        # Сохранение продуктов в базе данных
        Product.objects.bulk_create(products)
