from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'college']

class ProfileUpdateForm(forms.ModelForm):
    """ユーザー情報更新フォーム"""
    class Meta:
        model = CustomUser
        fields = ['username', 'college']

    def __init__(self, username=None, college=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if username:
            self.fields['username'].widget.attrs['value'] = username
        if college:
            self.fields['college'].widget.attrs['value'] = college
    
    def update(self, user):
        user.username = self.cleaned_data['username']
        user.college = self.cleaned_data['college']
        user.last_name = self.cleaned_data['last_name']
        user.save()

class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'college', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
