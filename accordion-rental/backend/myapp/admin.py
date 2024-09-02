# myapp/admin.py
from django.contrib import admin
from .models import Model, Rendipillid, Agreements, Invoices


admin.site.register(Model)
admin.site.register(Rendipillid)
admin.site.register(Agreements)
admin.site.register(Invoices)
