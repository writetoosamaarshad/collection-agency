from django.contrib import admin
from .models import Consumer, Client, Agency

# Register your models here to make them available in the Django admin interface.
admin.site.register(Consumer)
admin.site.register(Client)
admin.site.register(Agency)
