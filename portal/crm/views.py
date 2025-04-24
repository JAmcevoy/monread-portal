# crm/views.py
from django.shortcuts import render
from .models import Contact

def search_customer(request):
    contact = None
    query = request.GET.get('email')

    if query:
        try:
            contact = Contact.objects.get(email__iexact=query)
        except Contact.DoesNotExist:
            contact = None

    return render(request, 'crm/customer_info.html', {'contact': contact})
