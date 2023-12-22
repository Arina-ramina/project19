from django.urls import path, include

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, products, index, category, category_catalog

app_name = CatalogConfig.name


urlpatterns = [
    path('contacts/', contacts, name='contacts'),
    path('home/', home, name='home'),
    path('products/', products, name='products'),
    path('index/', index, name='index'),
    path ('category/', category, name='category'),
    path ('<int:pk>/catalog/', category_catalog, name='category_catalog'),
]
