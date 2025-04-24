# crm/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_customer, name='search_customer'),
]
