from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    )
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = '이름'
        self.fields['username'].label = '아이디'
        self.fields['email'].label = '이메일'
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'style': 'border-color: darkgreen;',
                'placeholder': '이름'
            }
        )
    )
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'style': 'border-color: darkgreen;',
                'placeholder': 'ID'
            }
        )
    )
    email = forms.EmailField(
        max_length=254,
        help_text='유효한 이메일을 입력해주세요. 해당 이메일로 인증 메일이 발송됩니다.',
        widget=forms.TextInput(
            attrs={
                'style': 'border-color: darkgreen',
                'placeholder': '이메일',
            })
    )
    password1 = forms.CharField(
        max_length=30,
        help_text='다른 개인정보와 비슷한 비밀번호는 사용할 수 없습니다. 비밀번호는 최소 8자 이상이어야 합니다. 비밀번호는 일상적으로 사용되는 비밀번호일 수 없습니다. 비밀번호는 전부 숫자로 할 수 없습니다.',
        widget=forms.TextInput(
            attrs={
                'style': 'border-color: darkgreen;',
                'placeholder': '비밀번호',
                'type': 'password',
            }
        )
    )
    password2 = forms.CharField(
        max_length=30,
        help_text='위와 동일한 비밀번호를 입력하세요.',
        widget=forms.TextInput(
            attrs={
                'style': 'border-color: darkgreen;',
                'placeholder': '비밀번호 확인',
                'type': 'password',
            }
        )
    )



    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('이미 가입된 이메일입니다.')
        return email


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': ("아이디 또는 비밀번호가 틀렸습니다."
                          ),
        'inactive': "이메일 인증을 완료해주세요. <buttton>이메일 재전송</button>",
    }
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'style': 'border-color: darkgreen;',
                'placeholder': 'ID'
            }
        )
    )
    password = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'style': 'border-color: darkgreen;',
                'placeholder': '비밀번호',
                'type': 'password',
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class SignUpProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'image',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','like_planning', 'like_club', 'like_info')
