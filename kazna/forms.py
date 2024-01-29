from django import forms
from .models import *
from client.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from bootstrap_datepicker_plus.widgets import DatePickerInput



class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'