from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Blog
from config import settings


# def category(request, pk):
#    category_item = Category.objects.get(pk=pk)
#    context = {'object_list': Product.objects.filter(category_id=pk),
#               'title': f'Наши товары по категориям {category_item.name}'}
#    return render(request, 'catalog/products.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя {name}, телефон {phone}, текст {message}')
    return render(request, 'catalog/contacts.html')


# def home(request):
#     products_list = Product.objects.all()[:100]
#     context = {'object_list': products_list}
#     return render(request, 'catalog/home.html', context)

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'


# def product(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     context = {
#         'product': product_item,
#         'title': f'Товар: {product_item.name}'
#     }
#     return render(request, 'catalog/product.html', context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'


class BlogCreateView(CreateView):
    model = Blog
    fields = ('name', 'content', 'preview',)
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        new_mat = form.save(commit=False)
        new_mat.slug = slugify(new_mat.name)
        new_mat.save()

        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        if self.object.views_count >= 101:
            send_mail(
                subject='Поздравление с 100 просмотрами',
                message='Ваша статья "{}" достигла 100 просмотров!'.format(self.object.name),
                from_email=settings.EMAIL_HOST_USER,  # Отправитель
                recipient_list=['arinafedor23@icloud.com']  # Получатель
            )

        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('name', 'content', 'preview',)
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        new_mat = form.save(commit=False)
        new_mat.slug = slugify(new_mat.name)
        new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        # Получаем обновленный объект после сохранения
        updated_obj = self.object
        # Формируем URL для перенаправления на страницу просмотра статьи
        return reverse('catalog:blog_view', kwargs={'slug': updated_obj.slug})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')
