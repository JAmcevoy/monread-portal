# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('contacts/<str:contact_id>/photo/', views.contact_photo, name='contact_photo'),
    path('/<str:contact_id>/', views.contact_detail, name='contact_detail'),
    path('', views.show_contacts, name='contacts'),  # URL to display contacts
    path('login/', views.contact_login, name='contact_login'),
]
