from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *


class StartQuestionForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['theme'].empty_lable = 'Тема'

    class Meta:
        model = Publication
        fields = ['theme', 'title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Кратко изложите суть вопроса'}),
            'content': forms.Textarea(attrs={'placeholder': 'Опишите подробно ваш вопрос'})
        }
        error_messages = {
            'theme': {
                'required': ("Тема не выбрана")
            },
            'title': {
                'required': ("Заголовок не может быть пустым")
            },
            'content': {
                'required': ("Вопрос не может быть пустым")
            }
        }


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Напишите ответ'})
        }
        error_messages = {
            'content': {
                'required': ("Ответ не может быть пустым")
            }
        }


class AddThemeForm(forms.ModelForm):

    class Meta:
        model = Theme
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Напишите название темы'}),
        }
        error_messages = {
            'name': {
                'required': ("Тема не может быть пустая")
            },
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
