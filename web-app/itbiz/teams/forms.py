from .models import Articles
from django.forms import ModelForm,TextInput, Textarea

class ArticlesForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'full_text', 'anons']
        widgets={
            'title': TextInput(attrs={
                'field-sizing': 'content',
                'class':'form-control',
                'placeholder':'Название статьи'
                }),

            'anons': TextInput(attrs={
                'field-sizing':'content',
                'class':'form-control',
                'placeholder':'Анонс статьи'
                }),
            'full-text': Textarea(attrs={
                'field-sizing': 'content',
                'class':'form-control',
                'placeholder':'Текст статьи'
                })
        }