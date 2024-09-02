from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('models/', views.ModelList.as_view(), name='model-list'),
    path('rendipillid/', views.RendipillidList.as_view(), name='rendipillid-list'),
]
