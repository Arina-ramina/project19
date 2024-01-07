from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from catalog.models import Product, Category


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя {name}, телефон {phone}, текст {message}')
    return render(request, 'catalog/contacts.html')


#class HomeListView(ListView):
#    model = Home
#    template_name = 'catalog/home.html'

def home(request):
    products_list = Product.objects.all()[:100]
    context = {'object_list': products_list}
    return render(request, 'catalog/home.html', context)


def product(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    context = {
        'product': product_item,
        'title': f'Товар: {product_item.name}'
    }
    return render(request, 'catalog/product.html', context)

class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category.html'
#def category(request):
#    context = {'object_list': Category.objects.all(),
#               'title': 'Продукты - Наши товары'}
#    return render(request, 'catalog/category.html', context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/home.html'

#def category_catalog(request, pk):
#    category_item = Category.objects.get(pk=pk)
#    context = {'object_list': Product.objects.filter(category_id=pk),
#               'title': f'Наши товары по категориям {category_item.name}'}
#    return render(request, 'catalog/products.html', context)