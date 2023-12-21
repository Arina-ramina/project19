from django.contrib import admin
from catalog.models import Product, Category

#admin.site.register(Product)
#admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price_for_one', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'title')


