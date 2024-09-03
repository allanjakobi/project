from django.contrib import admin
from django.urls import path, include
#from django.http import HttpResponseRedirect
from myapp import views
from .views import RendipillidListCreate

urlpatterns = [
    path('', RendipillidListCreate.as_view(), name='rendipillid-list'),  # Home view or main view
    path('admin/', admin.site.urls),  # Admin URL
    path('models/', views.ModelList.as_view(), name='model-list'),  # Model list view
    path('rendipillid/', views.RendipillidList.as_view(), name='rendipillid-list'),  # Rendipillid list view
    path('invoices/', views.InvoiceList.as_view(), name='invoice-list'),  # Invoice list view
    path('invoices/add/', views.InvoiceCreate.as_view(), name='invoice-add'),  # Invoice creation view
    path('invoices/<int:pk>/', views.InvoiceDetail.as_view(), name='invoice-detail'),  # Invoice detail view
    path('invoices/<int:pk>/edit/', views.InvoiceUpdate.as_view(), name='invoice-edit'),  # Invoice update view
]
