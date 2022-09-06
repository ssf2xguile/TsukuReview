from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
     get_user_model, logout as auth_logout,
)
from .forms import UserCreateForm

User = get_user_model() # 自作したUserモデルを使用するための宣言

class SignUpView(CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        return redirect('login')

class LoginView(LoginView):
    template_name = 'accounts/login.html'

class LogoutView(LogoutView):
    template_name = 'accounts/logout.html'

class ProfileView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        return render(self.request,'registration/profile.html')


class DeleteView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        user = User.objects.get(email=self.request.user.email)
        user.is_active = False
        user.save()
        auth_logout(self.request)
        return render(self.request,'registration/delete_complete.html')