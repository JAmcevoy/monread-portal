# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('contacts/', views.show_contacts, name='show_contacts'),  # URL to display contacts
    path('refresh-token/', views.refresh_access_token, name='refresh_access_token'),  # URL to refresh the access token
]
