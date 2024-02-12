from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Blog, Version
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

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/home.html'


# def product(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     context = {
#         'product': product_item,
#         'title': f'Товар: {product_item.name}'
#     }
#     return render(request, 'catalog/product.html', context)

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_versions'] = Version.objects.filter(product=self.object)
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Чтобы добавить продукт, сначала войдите в систему.')
            return redirect('users:login')  # Перенаправление на страницу входа
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ('name', 'title', 'price_for_one', 'preview')
    success_url = reverse_lazy('catalog:home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Чтобы добавить продукт, сначала войдите в систему.')
            return redirect('users:login')  # Перенаправление на страницу входа
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        # Получаем активные версии продукта
        active_versions = Version.objects.filter(product=self.object, is_current=True)

        # Передаем активные версии в контекст представления
        context_data['active_versions'] = active_versions

        # Создаем формсет версий продукта
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        self.object.owner = self.request.user
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


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
        slug = self.kwargs.get('slug')
        if slug:
            self.object = get_object_or_404(Blog, slug=slug)
        else:
            pk = self.kwargs.get('pk')
            self.object = get_object_or_404(Blog, pk=pk)
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
        return reverse('catalog:blog_view_slug', kwargs={'slug': updated_obj.slug})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')

# def add_version(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         form = VersionForm(request.POST)
#         if form.is_valid():
#             version = form.save(commit=False)
#             version.product = product
#             version.save()
#             return redirect('catalog:product', pk=product.pk)
#     else:
#         form = VersionForm()
#     return render(request, 'product_form.html', {'form': form})


class AddVersionView(View):
    model = Version
    template_name = 'catalog/product_form.html'  # Используем тот же шаблон, что и для редактирования продукта
    form_class = VersionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        context['product'] = product
        context['product_form'] = ProductForm(instance=product)

        # Предзаполнение формы версии данными о продукте
        initial_data = {
            'product': product,
            'No_version': product.versions.count() + 1,
        }
        context['version_form'] = VersionForm(initial=initial_data)
        return context
