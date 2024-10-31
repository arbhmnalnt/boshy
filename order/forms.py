from django import forms
from .models import *
from client.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from bootstrap_datepicker_plus.widgets import DatePickerInput

class MasterInvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clientMI'].queryset = Client.objects.all().order_by('-created_at')


    class Meta:
        model = MasterInvoice
        fields = '__all__'


class DetailedOrderForm(forms.ModelForm):
    storge = forms.CharField(max_length=10000, label="الكمية فى المخزن")
    remain = forms.CharField(max_length=10000, label="الكمية المتبقية")
    class Meta:
        model = DetailedOrder
        fields = ['masterInvoice','name', 'img', 'clothD','used','storge','remain','details']    


class basicInvoiceInfoForm(forms.Form): 
    masterInvoice   = forms.ModelChoiceField(queryset=MasterInvoice.objects.all(), label="الفاتورة")
    total           = forms.IntegerField(required=False, label="المبلغ الإجمالى")
    paid            = forms.IntegerField(required=False, label="المبلغ المدفوع")
    remain          = forms.IntegerField(required=False, label="المبلغ المتبقى")
    clientS         = forms.ModelChoiceField(queryset=Client.objects.all(), label="اسم العميل", to_field_name='id')
    tall            = forms.CharField(max_length=15,  required=False, label="الطول") # الطول
    sadr            = forms.CharField(max_length=15,  required=False, label="الصدر") # الصدر
    kom             = forms.CharField(max_length=15,  required=False, label="الكم") # الكم
    ktf             = forms.CharField(max_length=15,  required=False, label="الكتف") # الكتف
    t               = forms.CharField(max_length=15,  required=False, label="T") # دوران الرقبة
    leaka           = forms.CharField(max_length=15,  required=False, label="اللياقه") # اللياقه
    kazna           = forms.CharField(max_length=15,  required=False, label="الخزنه") # الخزنه
    atak            = forms.CharField(max_length=15,  required=False, label="الأتك") # الأتك
    statue          = forms.ChoiceField(choices=basicInvoiceInfo.orderStatue, required=False, label="حالة الطلب", initial='unknwon')
    receve_date = forms.DateField( required=False, label="تاريخ التسليم", widget=DatePickerInput())

    def clean(self):
        cleaned_data = super().clean()
        total   = cleaned_data.get('total')
        paid    = cleaned_data.get('paid')

        if total is not None and paid is not None:
            remain = total - paid
            cleaned_data['remain'] = remain

        return cleaned_data

class DeliverdForm(forms.ModelForm):
    class Meta:
        model = Deliverd
        fields = '__all__'

class DebitForm(forms.ModelForm):
    class Meta:
        model  = DebitOrder
        fields  = ['MasterInvoice', 'paid', 'remain', 'total']
