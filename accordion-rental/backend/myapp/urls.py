from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AvailableInstrumentsViewSet, RendipillidListCreate, logout_user, register_user, login_user, profile_view, test_auth_view, contracts_view, ReserveInstrumentView
from .views import upload_payments, list_agreements, send_email, update_agreement_info

from django.contrib import admin
from .views import admin_view, get_csrf_token, csrf
from django.conf import settings
from django.conf.urls.static import static

# Create a router and register your viewsets with it
router = DefaultRouter()
router.register(r'available-instruments', AvailableInstrumentsViewSet, basename='available-instruments')

urlpatterns = [
    # Main view for listing and creating rendipillid
    path('', RendipillidListCreate.as_view(), name='rendipillid-list'),
    
    # Admin URL
    path('admin/', admin.site.urls),
    

    # Other views
    path('api/test-auth/', test_auth_view, name='test_auth_view'),
    path('models/', views.ModelList.as_view(), name='model-list'),
    path('rendipillid/', views.RendipillidList.as_view(), name='rendipillid-list'),
    path('api/get_csrf_token/', get_csrf_token, name='get_csrf_token'),
    path('api/register/', register_user, name='register_user'),
    path('api/profile/', profile_view, name='profile_view'),
    path('api/logout/', logout_user, name='logout_user'),
    path('api/agreements/', views.create_agreement, name='create_agreement'),
    path('api/contracts/', views.contracts_view, name='contracts_view'),
    path('api/invoices/', views.invoices_view, name='invoices_view'),
    path('api/invoices/download/<int:invoice_id>/', views.download_invoice, name='download_invoice'),
    path('api/rates/<int:price_level_id>/', views.get_rate, name='get_rate'),
    path('api/contracts/download/<int:contract_id>/', views.download_contract, name='download_contract'),
    path('api/instruments/<int:instrument_id>/reserve', ReserveInstrumentView.as_view(), name='reserve_instrument'),
    path('api/login/', login_user, name='login_user'),
    path('api/check_login/', views.check_login, name='check_login'),
    path('admin-view/', admin_view, name='admin_view'),
    path('invoices/', views.InvoiceList.as_view(), name='invoice-list'),
    path('invoices/add/', views.InvoiceCreate.as_view(), name='invoice-add'),
    path('invoices/<int:pk>/', views.InvoiceDetail.as_view(), name='invoice-detail'),
    path('invoices/<int:pk>/edit/', views.InvoiceUpdate.as_view(), name='invoice-edit'),
    path('csrf/', get_csrf_token),
    path('api/csrf/', csrf),
    path('api/admin/upload-payments/', upload_payments, name='upload_payments'),

    # Endpoint to fetch agreements
    path('api/admin/agreements/', list_agreements, name='list_agreements'),

    # Endpoint to send email for a specific agreement
    path('api/admin/send-email/<int:agreement_id>/', views.send_email, name='send-email'),
    path('api/admin/update-info/<int:agreement_id>/', update_agreement_info, name='update_agreement_info'),


    # Include the router URLs
    path('api/', include(router.urls)),  # Use this for the API endpoint
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
