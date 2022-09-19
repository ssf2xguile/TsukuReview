import email
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
import re

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
            self.fields['college'].initial = college
    
    def update(self, user):
        user.username = self.cleaned_data['username']
        user.college = self.cleaned_data['college']
        user.save()

class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'college', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        print(username)
        if len(username) <= 1:
            raise forms.ValidationError('名前が短すぎます')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        email_pattern = r"s1[8-9]|s2[0-2]\d{5}@[su].tsukuba.ac.jp"
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('このメールアドレスは既に登録されています')
        if re.match(email_pattern, email) is None:
            raise forms.ValidationError('sから始まる大学のメールアドレスを入力してください')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません")
        return password2

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
    
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError('メールアドレスまたはパスワードが間違っています')
        if user.password != password:
            raise forms.ValidationError('メールアドレスまたはパスワードが間違っています')

class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
