from django import forms
from .models import Info_Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Info_Article
        exclude = ('like_set','author')