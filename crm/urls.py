# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('contacts/<str:contact_id>/photo/', views.contact_photo, name='contact_photo'),
    path('contacts/<str:contact_id>/', views.contact_detail, name='contact_detail'),
    path('contacts/', views.show_contacts, name='show_contacts'),  # URL to display contacts
    path('login/', views.contact_login, name='contact_login'),
]
