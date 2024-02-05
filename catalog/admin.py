from django.contrib import admin
from catalog.models import Product, Category, Blog, Version


# admin.site.register(Product)
# admin.site.register(Category)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'title')
    list_filter = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price_for_one', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'title')



@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'No_version', 'name_version', 'is_current')
    list_filter = ('product', 'name_version', 'No_version', 'is_current',)
    search_fields = ('product', 'title', 'is_current')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'content')
    list_filter = ('name',)
