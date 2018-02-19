from django import forms

from .models import Create_Post

class Create_PostForm(forms.ModelForm):

#class Meta: 이 폼을 만들기 위해서 어떤 모델이 쓰여야 하는지 장고에 알려주는 구문
    class Meta:
        model = Create_Post
        fields = '__all__'

#class ImageExampleForm(forms.ModelForm):
    #class Meta:
        #model = ImageExample
        #fields = ['image']

