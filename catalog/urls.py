from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, ProductDetailView, \
    BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, \
    ProductCreateView, ProductUpdateView, AddVersionView

app_name = CatalogConfig.name

urlpatterns = [
    path('contacts/', contacts, name='contacts'),
    path('', ProductListView.as_view(), name='home'),
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('home/', ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('product/<int:pk>/add_version/', AddVersionView.as_view(), name='add_version'),
    path('product_edit/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),  # редактирование продукта
    path('create/', BlogCreateView.as_view(), name='blog_create'),  # создать блог
    path('list/', BlogListView.as_view(), name='blog_list'),  # отображение списка объектов
    path('view/<int:pk>/', BlogDetailView.as_view(), name='blog_view_pk'),  # просмотр деталей c pk
    path('view/<slug:slug>/', BlogDetailView.as_view(), name='blog_view_slug'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='blog_edit'),  # редактирование
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),  # удалить
]
