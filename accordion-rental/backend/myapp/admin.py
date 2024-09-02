# myapp/admin.py
from django.contrib import admin
from .models import Model, Rendipillid, Agreements, Invoices, Users, Rates

class RendipillidAdmin(admin.ModelAdmin):
    list_display = ('instrumentId', 'color', 'get_model_details')
    
    def get_model_details(self, obj):
        return f"{obj.modelId.brand} {obj.modelId.model}"
    get_model_details.short_description = 'Model Name'

class UsersAdmin(admin.ModelAdmin):
    list_display = ('userId', 'firstName', 'lastName')

admin.site.register(Model)
admin.site.register(Rendipillid, RendipillidAdmin)
admin.site.register(Agreements)
admin.site.register(Invoices)
admin.site.register(Users)  # Register the Users model
admin.site.register(Rates) 
