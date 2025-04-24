from django.urls import path
from . import views

urlpatterns = [
    path('customer_info/', views.customer_info, name='customer_info'),
]
