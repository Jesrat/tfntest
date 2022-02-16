from .models import (Customer, CustomerAddress, CustomerDocument)
from django.contrib import admin

# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerAddress)
admin.site.register(CustomerDocument)
