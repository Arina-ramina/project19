from django.urls import path, include

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, product, CategoryListView, ProductDetailView
from . import views

app_name = CatalogConfig.name


urlpatterns = [
    path('contacts/', contacts, name='contacts'),
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('product/<int:pk>/', views.product, name='product'),
    path ('category/', CategoryListView.as_view(), name='category'),
    path ('<int:pk>/catalog/', ProductDetailView.as_view(), name='category_catalog'),
]
