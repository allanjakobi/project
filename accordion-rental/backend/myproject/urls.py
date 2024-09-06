from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Root URL shows rendipillid list
    path('', include('myapp.urls')),  # Includes URLs from the `myapp`
]
