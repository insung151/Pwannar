from django import forms
from .models import Info_Article, Info_Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Info_Article
        exclude = ('like_set', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Info_Comment
        exclude = ('article', 'author', )