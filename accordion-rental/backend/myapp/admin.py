# myapp/admin.py
from django.contrib import admin
from .models import Model, Rendipillid, Agreements, Invoices, Users, Rates

class RendipillidAdmin(admin.ModelAdmin):
    list_display = ('instrumentId', 'color', 'get_model_details')
    
    def get_model_details(self, obj):
        return f"{obj.modelId.brand} {obj.modelId.model}"
    get_model_details.short_description = 'Model Name'

class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'email', 'phone', 'country', 'province', 'municipality',
        'settlement', 'street', 'house', 'apartment'
    )
    list_filter = ('country', 'province', 'municipality', 'settlement')
    search_fields = ('firstName', 'lastName', 'email', 'phone')

    def full_name(self, obj):
        return f"{obj.firstName} {obj.lastName}"
    full_name.admin_order_field = 'firstName'  # Sorts by first name
    full_name.short_description = 'Full Name'

admin.site.register(Users, UsersAdmin)

admin.site.register(Model)
admin.site.register(Rendipillid, RendipillidAdmin)
admin.site.register(Agreements)
admin.site.register(Invoices)
admin.site.register(Rates) 
