from django.shortcuts import render

from catalog.models import Product, Category


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя {name}, телефон {phone}, текст {message}')
    return render(request, 'catalog/contacts.html')


def home(request):
    return render(request, 'catalog/home.html')


def products(request):
    context = {'object_list': Product.objects.all(),
               'title': 'Продукты - Наши товары'}
    return render(request, 'catalog/products.html', context)


def index(request):
    context = {'object_list': Category.objects.all(),
               'title': 'Продукты - Наши категории'}
    return render(request, 'catalog/index.html', context)

def category(request):
    context = {'object_list': Category.objects.all(),
               'title': 'Продукты - Наши товары'}
    return render(request, 'catalog/category.html', context)

def category_catalog(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {'object_list': Product.objects.filter(category_id=pk),
               'title': f'Наши товары по категориям {category_item.name}'}
    return render(request, 'catalog/products.html', context)