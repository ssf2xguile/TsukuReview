from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile_edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_reset/', views.PasswordResetView.as_view(extra_email_context={'domain': '127.0.0.1:8000'}), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/done', views.SignUpDoneView.as_view(), name='signup_done'),
    path('signup/complete/<token>/', views.SignUpCompleteView.as_view(), name='signup_complete'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('<int:pk>/delete_confirm', views.DeleteConfirmView.as_view(), name='delete_confirm'),
    path('delete_complete', views.DeleteCompleteView.as_view(), name='delete_complete'),
    path('notices/', views.NoticesView.as_view(), name='staff_notices'),
    path('notice/create/', views.NoticeCreateView.as_view(), name='staff_notice_create'),
    path('notice/update/<int:pk>/', views.NoticeUpdateView.as_view(), name='staff_notice_update'),
    path('notice/delete/<int:pk>/', views.NoticeDeleteView.as_view(), name='staff_notice_delete'),
]