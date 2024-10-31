from django import forms
from .models import *
from client.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from bootstrap_datepicker_plus.widgets import DatePickerInput

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        
class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'