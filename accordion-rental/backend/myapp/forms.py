from django import forms
from .models import Rendipillid

class RendipillidForm(forms.ModelForm):
    class Meta:
        model = Rendipillid
        fields = '__all__'

# myapp/views.py (if using Django template)
from django.shortcuts import render
from .forms import RendipillidForm

def rendipillid_create(request):
    if request.method == "POST":
        form = RendipillidForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RendipillidForm()

    return render(request, 'rendipillid_form.html', {'form': form})