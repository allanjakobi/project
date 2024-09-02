
from django.contrib import admin
from django.urls import path, include
from myapp.views import RendipillidList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RendipillidList.as_view(), name='rendipillid-list'),  # Root URL shows all rendipillid
    path('models/', include('myapp.urls')),  # Assuming other URLs are handled similarly
]
