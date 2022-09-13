from django import forms
from .models import *


class StartThemeForm(forms.ModelForm):
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
