from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'college']

# class SignupUserForm(SignupForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'college', 'email']
    
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         existing = CustomUser.objects.filter(
#             email=email
#         ).exists()
#         if existing:
#             forms.ValidationError('このメールアドレスは既に登録されています')
#         return email

#     def save(self, request):
#         user = super(SignupUserForm, self).save(request)
#         user.username = self.cleaned_data['username']
#         user.college = self.cleaned_data['college']
#         user.email = self.cleaned_data['email']
#         user.save()
#         return user


class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'college', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)