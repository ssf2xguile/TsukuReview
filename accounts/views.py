from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View, FormView
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
     get_user_model, logout as auth_logout,
)

from accounts.models import CustomUser
from .forms import UserCreateForm, ProfileUpdateForm, MyPasswordChangeForm, UserLoginForm

User = get_user_model() # 自作したUserモデルを使用するための宣言

class SignUpView(CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        return redirect('login')

class LoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = UserLoginForm

class LogoutView(LogoutView):
    template_name = 'accounts/logout.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    form_class = ProfileUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ProfileEditView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile_edit.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'username' : self.request.user.username,
            'college' : self.request.user.college,
        })
        return kwargs

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('profile')
    template_name = 'accounts/password_change.html'

class DeleteConfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/delete_confirm.html'

class UserDeleteView(LoginRequiredMixin, View):

    # アカウントごと削除
    def get(self, *args, **kwargs):
        CustomUser.objects.filter(email=self.request.user.email).delete()
        auth_logout(self.request)
        return render(self.request,'accounts/delete_complete.html')