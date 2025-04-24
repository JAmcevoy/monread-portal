# crm/models.py
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=255)
    support_time_left = models.CharField(max_length=100)

    def __str__(self):
        return self.name
