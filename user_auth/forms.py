from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import UserExtended


class UserSignUp(forms.Form):
    email = forms.EmailField(required=False, label='E-mail', widget=forms.EmailInput(attrs={
        'class': 'sign-up-field',
        'placeholder': 'example@domain.com'
    }))
    f_name = forms.CharField(required=False, label='Имя', widget=forms.TextInput(attrs={
        'class': 'sign-up-field',
        'placeholder': 'Имя с большой буквы'
    }))
    s_name = forms.CharField(required=False, label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'sign-up-field',
        'placeholder': 'Фамилия с большой буквы'
    }))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'sign-up-field',
        'placeholder': 'От 8 до 16 символов'
    }), label='Пароль')
    confirm_pwd = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'sign-up-field'
    }), label='Подтв. пароля')

    def clean_f_name(self):
        f_name = self.cleaned_data.get('f_name')
        if not f_name:
            raise forms.ValidationError('Это обязательное поле')
        if len(f_name) > 18:
            raise forms.ValidationError('Имя должно быть не длиннее 18 символов')
        if len(f_name.split()) > 1:
            raise forms.ValidationError('Имя должно состоять из одного слова')
        if not f_name.isalpha():
            raise forms.ValidationError('Имя должно состоять только из букв')
        if not (f_name[0].isupper() and f_name[1:].islower()):
            raise forms.ValidationError('Имя должно начинаться со своей единственной заглавной буквы')
        return f_name

    def clean_s_name(self):
        s_name = self.cleaned_data.get('s_name')
        if not s_name:
            raise forms.ValidationError('Это обязательное поле')
        if len(s_name) > 18:
            raise forms.ValidationError('Фамилия должна быть не длиннее 18 символов')
        if len(s_name.split()) > 1:
            raise forms.ValidationError('Фамилия должна состоять из одного слова')
        if not s_name.isalpha():
            raise forms.ValidationError('Фамилия должна состоять только из букв')
        if not (s_name[0].isupper() and s_name[1:].islower()):
            raise forms.ValidationError('Фамилия должна начинаться со своей единственной заглавной буквы')
        return s_name

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Это обязательное поле')
        if len(password) < 8 or len(password) > 16:
            raise forms.ValidationError('Пароль должен содержать от 8 до 16 символов')
        return password

    def clean_confirm_pwd(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('confirm_pwd')
        if p1 != p2:
            raise forms.ValidationError('Поля должны совпадать')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Это обязательное поле')
        users = UserExtended.objects.filter(base_user__email=email)
        if users.exists():
            raise forms.ValidationError(f'Данный e-mail уже зарегистрирован')
        return email


class SignInForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "class": "sign-in-field",
        "placeholder": "E-mail",
    }))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "class": "sign-in-field",
            "placeholder": "Пароль",
        }),
    )
