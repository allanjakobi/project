from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from myapp import views
from .views import RendipillidListCreate

urlpatterns = [
    path('', RendipillidListCreate.as_view(), name='rendipillid-list'),
    path('admin/', admin.site.urls),
    path('models/', views.ModelList.as_view(), name='model-list'),
    path('rendipillid/', views.RendipillidList.as_view(), name='rendipillid-list'),
]
