from django import forms

from catalog.models import Product, Version


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['owner']

    def clean_name(self):
        name = self.cleaned_data['name']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in name.lower():
                raise forms.ValidationError(f'Название содержит запрещенное слово: {word}')
        return name

    def clean_description(self):
        description = self.cleaned_data['title']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in description.lower():
                raise forms.ValidationError(f'Описание содержит запрещенное слово: {word}')
        return description


class VersionForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'


class MProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('is_published', 'title', 'category')
