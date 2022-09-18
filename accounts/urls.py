from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile_edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('delete_confirm', views.DeleteConfirmView.as_view(), name='delete_confirm'),
    path('delete_complete', views.UserDeleteView.as_view(), name='delete_complete'),
]