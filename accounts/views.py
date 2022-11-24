from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View, FormView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
     get_user_model, logout as auth_logout,
)
from django.utils import timezone
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from accounts.models import CustomUser, Notice
from .mixins import OnlyStaffMixin
from .forms import UserCreateForm, ProfileUpdateForm, MyPasswordChangeForm, UserLoginForm, NoticeForm, MySetPasswordForm, MyPasswordResetForm

User = get_user_model() # 自作したUserモデルを使用するための宣言

class SignUpView(CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        local_host = '127.0.0.1:8000'
        context = {
            'protocol': self.request.scheme,
            'domain': local_host,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('accounts/mail_template/create/subject.txt', context)
        message = render_to_string('accounts/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('signup_done')

        # サインアップしてすぐにログインするための処理
        # user = form.save()
        # return redirect('login')
    
class SignUpDoneView(TemplateView):
    template_name = 'accounts/signup_done.html'

class SignUpCompleteView(TemplateView):
    template_name = 'accounts/signup_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)

    def get(self, request, *args, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

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

class PasswordResetView(PasswordResetView):
    subject_template_name = 'accounts/mail_template/password_reset/subject.txt'
    email_template_name = 'accounts/mail_template/password_reset/message.txt'
    template_name = 'accounts/password_reset.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    template_name = 'accounts/password_reset_confirm.html'
    form_class = MySetPasswordForm
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'accounts/password_reset_complete.html'


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