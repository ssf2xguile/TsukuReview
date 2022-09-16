from django.urls import path

from . import views, apis

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('lecture/<str:pk>/', views.LectureView.as_view(), name='lecture'),
    path('api/search_subjects', apis.SearchSubjectAPI.as_view(), name = "api_search_subjects"),
]