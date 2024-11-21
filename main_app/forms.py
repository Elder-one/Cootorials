from django import forms
from .models import RecipeCategory


class NewRecipeForm(forms.Form):
    title = forms.CharField(required=False, label='Название', widget=forms.Textarea(attrs={
        'class': 'new-recipe-text-field',
        'placeholder': 'Название блюда',
        'rows': '3',
    }))
    description = forms.CharField(required=False, label='Описание', widget=forms.Textarea(attrs={
        'class': 'new-recipe-text-field',
        'placeholder': 'Краткое описание',
        'rows': '5'
    }))
    tutorial = forms.CharField(required=False, label='Шаги приготовления', widget=forms.Textarea(attrs={
        'class': 'new-recipe-text-field',
        'placeholder': 'Шаги приготовления',
        'rows': '7'
    }))
    category = forms.ChoiceField(choices=((categ.name, categ.name) for categ in RecipeCategory.objects.all()),
                                 widget=forms.Select(attrs={
                                     'class': 'new-recipe-choice-field',
                                     'placeholder': 'Выберите',
                                 }))
    image = forms.ImageField(required=True, label='Изображение', widget=forms.FileInput(attrs={
        'class': 'new-recipe-image-field',
    }))

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Это обязательное поле')
        if len(title) > 150:
            raise forms.ValidationError('Не более 150 символов')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError('Это обязательное поле')
        if len(description) > 150:
            raise forms.ValidationError('Не более 250 символов')
        return description

    def clean_tutorial(self):
        tutorial = self.cleaned_data.get('tutorial')
        if not tutorial:
            raise forms.ValidationError('Это обязательное поле')
        return tutorial

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('Выберите категорию блюда')
        return category

