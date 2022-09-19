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
            'title': forms.TextInput(),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'answer-textarea', 'placeholder': 'Напишите ответ'})
        }
        error_messages = {
            'content': {
                'required': ("Ответ не может быть пустым")
            }
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
