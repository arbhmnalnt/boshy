from django import forms
from .models import *
from client.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit



class MasterInvoiceForm(forms.ModelForm):
    class Meta:
        model = MasterInvoice
        fields = '__all__'


class DetailedOrderForm(forms.ModelForm):
    class Meta:
        model = DetailedOrder
        fields = '__all__'
    


class basicInvoiceInfoForm(forms.Form): 
    masterInvoice   = forms.ModelChoiceField(queryset=MasterInvoice.objects.all(), label="الفاتورة")
    total           = forms.DecimalField(max_digits=3, decimal_places=2, required=False, label="المبلغ الإجمالى")
    paid            = forms.DecimalField(max_digits=3, decimal_places=2, required=False, label="المبلغ المدفوع")
    remain          = forms.DecimalField(max_digits=3, decimal_places=2, required=False, label="المبلغ المتبقى")
    clientS         = forms.ModelChoiceField(queryset=Client.objects.all(), label="اسم العميل")
    tall            = forms.CharField(max_length=5,  required=False, label="الطول") # الطول
    kom             = forms.CharField(max_length=5,  required=False, label="الكم") # الكم
    ktf             = forms.CharField(max_length=5,  required=False, label="الكتف") # الكتف
    sadr            = forms.CharField(max_length=5,  required=False, label="الصدر") # الصدر
    leaka           = forms.CharField(max_length=5,  required=False, label="اللياقه") # اللياقه
    kazna           = forms.CharField(max_length=5,  required=False, label="الخزنه") # الخزنه
    atak            = forms.CharField(max_length=5,  required=False, label="الأتك") # الأتك

    def clean(self):
        cleaned_data = super().clean()
        total   = cleaned_data.get('total')
        paid    = cleaned_data.get('paid')

        if total is not None and paid is not None:
            remain = total - paid
            cleaned_data['remain'] = remain

        return cleaned_data