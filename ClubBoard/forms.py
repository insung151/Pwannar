from django import forms

from .models import Create_Post


class Create_PostForm(forms.ModelForm):
    class Meta:
        model = Create_Post
        exclude = ['view_count', 'like_set', 'author']
