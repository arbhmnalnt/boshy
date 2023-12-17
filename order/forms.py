from django import forms
from .models import *


class MasterInvoiceForm(forms.ModelForm):
    class Meta:
        model = MasterInvoice
        fields = '__all__'

class DetailedOrderForm(forms.ModelForm):
    class Meta:
        model = DetailedOrder
        fields = '__all__'