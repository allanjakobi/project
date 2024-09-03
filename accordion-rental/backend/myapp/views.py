from rest_framework import generics
from .models import Model, Rendipillid
from .serializers import ModelSerializer, RendipillidSerializer
from django.shortcuts import render
from .forms import RendipillidForm
from .models import Rendipillid
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Invoices

class InvoiceList(ListView):
    model = Invoices
    template_name = 'invoices/invoice_list.html'  # Adjust to your template path
    context_object_name = 'invoices'

class InvoiceDetail(DetailView):
    model = Invoices
    template_name = 'invoices/invoice_detail.html'  # Adjust to your template path

class InvoiceCreate(CreateView):
    model = Invoices
    fields = ['date', 'agreementId', 'quantity', 'price']  # Adjust fields to your model
    template_name = 'invoices/invoice_form.html'  # Adjust to your template path
    success_url = reverse_lazy('invoice-list')

class InvoiceUpdate(UpdateView):
    model = Invoices
    fields = ['date', 'agreementId', 'quantity', 'price']  # Adjust fields to your model
    template_name = 'invoices/invoice_form.html'  # Adjust to your template path
    success_url = reverse_lazy('invoice-list')

class ModelList(generics.ListCreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

class RendipillidList(generics.ListCreateAPIView):
    queryset = Rendipillid.objects.all()
    serializer_class = RendipillidSerializer

class RendipillidListCreate(generics.ListCreateAPIView):
    queryset = Rendipillid.objects.all()
    serializer_class = RendipillidSerializer


def rendipillid_create(request):
    if request.method == "POST":
        form = RendipillidForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RendipillidForm()

    return render(request, 'rendipillid_form.html', {'form': form})

""" class RendipillidList(generics.ListAPIView):
    queryset = Rendipillid.objects.all()
    serializer_class = RendipillidSerializer """

def rendipillid_list_view(request):
    # Fetch all rendipillid entries, including related model data
    rendipillid_list = Rendipillid.objects.select_related('modelId').all()
    return render(request, 'rendipillid_list.html', {'rendipillid_list': rendipillid_list})

