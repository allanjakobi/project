from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from datetime import date
from .models import Agreements, Rendipillid




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

class AgreementForm(forms.ModelForm):
    months = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(60)],
        widget=forms.NumberInput(attrs={'min': 1, 'max': 60}),
        initial=12
    )
    startDate = forms.DateField(
        widget=forms.DateInput(format='%d.%m.%Y', attrs={'placeholder': 'DD.MM.YYYY'}),
        input_formats=['%d.%m.%Y'],
        initial=date.today,
        help_text=mark_safe("Format: <strong>DD.MM.YYYY</strong>")
    )

    class Meta:
        model = Agreements
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter to show only instruments with status "Available"
        self.fields['instrumentId'].queryset = Rendipillid.objects.filter(status="Available")
        
        # Set initial value for invoice_interval
        self.fields['invoice_interval'].initial = 1

        # Handle months field to update invoice_interval choices
        if self.is_bound:
            try:
                months = int(self.data.get('months', self.fields['months'].initial))
            except ValueError:
                months = self.fields['months'].initial
        else:
            months = self.instance.months if self.instance.pk else self.fields['months'].initial

        # Calculate valid divisors for invoice_interval
        valid_intervals = [i for i in range(1, months + 1) if months % i == 0]
        self.fields['invoice_interval'].choices = [(i, str(i)) for i in valid_intervals]

        # Restrict input to valid choices only
        self.fields['invoice_interval'].widget = forms.Select(choices=self.fields['invoice_interval'].choices)

    def clean_invoice_interval(self):
        invoice_interval = self.cleaned_data.get('invoice_interval')
        months = self.cleaned_data.get('months')
        
        if months % invoice_interval != 0:
            raise forms.ValidationError("Invalid interval selected for the given number of months.")
        
        return invoice_interval
