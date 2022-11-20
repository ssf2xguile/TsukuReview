from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View, FormView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
     get_user_model, logout as auth_logout,
)
from django.utils import timezone
from accounts.models import CustomUser, Notice
from .mixins import OnlyStaffMixin
from .forms import UserCreateForm, ProfileUpdateForm, MyPasswordChangeForm, UserLoginForm, NoticeForm

User = get_user_model() # 自作したUserモデルを使用するための宣言

class SignUpView(CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        return redirect('login')

class LoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

class LogoutView(LoginRequiredMixin, LogoutView):
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

class NoticesView(LoginRequiredMixin, OnlyStaffMixin, ListView):
    template_name = 'accounts/notices.html'
    model = Notice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notices'] = Notice.objects.all().order_by('-created_at')
        return context

class NoticeCreateView(LoginRequiredMixin, OnlyStaffMixin, CreateView):
    template_name = 'accounts/notice_create.html'
    form_class = NoticeForm
    success_url = reverse_lazy('staff_notices')

class NoticeUpdateView(LoginRequiredMixin, OnlyStaffMixin, UpdateView):
    template_name = 'accounts/notice_update.html'
    model = Notice
    fields = ('title', 'content')
    success_url = reverse_lazy('staff_notices')

    def form_valid(self, form):
        notice = form.save(commit=False)
        notice.updated_at = timezone.now()
        notice.save()
        return redirect('staff_notices')

class NoticeDeleteView(LoginRequiredMixin, OnlyStaffMixin, DeleteView):
    template_name = 'accounts/notice_delete.html'
    model = Notice
    success_url = reverse_lazy('staff_notices')