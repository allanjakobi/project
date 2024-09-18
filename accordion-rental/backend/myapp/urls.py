from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AvailableInstrumentsViewSet, RendipillidListCreate, register_user, login_user
from django.contrib import admin
from .views import admin_view, get_csrf_token



# Create a router and register your viewsets with it
router = DefaultRouter()
router.register(r'available-instruments', AvailableInstrumentsViewSet, basename='available-instruments')

urlpatterns = [
    # Main view for listing and creating rendipillid
    path('', RendipillidListCreate.as_view(), name='rendipillid-list'),
    
    # Admin URL
    path('admin/', admin.site.urls),
    

    # Other views
    path('models/', views.ModelList.as_view(), name='model-list'),
    path('rendipillid/', views.RendipillidList.as_view(), name='rendipillid-list'),
    path('api/register/', register_user, name='register_user'),
    path('api/login/', login_user, name='login_user'),
    path('admin-view/', admin_view, name='admin_view'),
    path('invoices/', views.InvoiceList.as_view(), name='invoice-list'),
    path('invoices/add/', views.InvoiceCreate.as_view(), name='invoice-add'),
    path('invoices/<int:pk>/', views.InvoiceDetail.as_view(), name='invoice-detail'),
    path('invoices/<int:pk>/edit/', views.InvoiceUpdate.as_view(), name='invoice-edit'),
    path('csrf/', get_csrf_token),

    # Include the router URLs
    path('api/', include(router.urls)),  # Use this for the API endpoint
]
