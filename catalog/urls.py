from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, ProductDetailView, \
    BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = CatalogConfig.name



urlpatterns = [
    path('contacts/', contacts, name='contacts'),
    path('', ProductListView.as_view(), name='home'),
    path('home/', ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('create/', BlogCreateView.as_view(), name='blog_create'), #создать
    path('list/', BlogListView.as_view(), name='blog_list'), #отображение списка объектов
    path('view/<slug:slug>/', BlogDetailView.as_view(), name='blog_view'), #просмотр деталей
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='blog_edit'), #редактирование
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'), #удалить
]
