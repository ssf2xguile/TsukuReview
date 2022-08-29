from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('lecture/', views.LectureView.as_view(), name='lecture'),
]