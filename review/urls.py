from django.urls import path

from . import views, apis

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('contacts/confirm/', views.ContactsConfirmView.as_view(), name='contacts_confirm'),
    path('contacts/complete/', views.ContactsCompleteView.as_view(), name='contacts_complete'),
    path('lecture/<str:pk>/', views.LectureView.as_view(), name='lecture'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('new_reviews/', views.NewReviewsView.as_view(), name='new_reviews'),
    path('api/search_subjects', apis.SearchSubjectAPI.as_view(), name = "api_search_subjects"),
    path('api/get_subject', apis.GetSubjectAPI.as_view(), name = "api_get_subject"),
]