from django import forms
from .models import *


class ClientForm(forms.ModelForm):
    FName    =   forms.CharField(label="الاسم الاول")
    SName    =   forms.CharField(label="الاسم الثانى")
    TName    =   forms.CharField(label="الاسم الثالث")
    LName    =   forms.CharField(label="الاسم الرابع")
    book     =   forms.CharField(label="الدفتر")
    page     =   forms.CharField(label="رقم الصفحة")
    phone    =   forms.CharField(label="رقم التليفون")
    address  =   forms.CharField(label="العنوان ")

    class Meta:
        model = Client
        fields = ['FName', 'SName', 'TName', 'LName', 'kindMale', 'book', 'page', 'phone', 'address']
    
    def clean(self):
        cleaned_data = super().clean()
        name = f"{cleaned_data.get('FName')} {cleaned_data.get('SName')} {cleaned_data.get('TName')} {cleaned_data.get('LName')}".strip()
        if Client.objects.filter(name=name).exists():
            raise forms.ValidationError("هذا العميل مسجل من قبل !")
        return cleaned_data

class ClientSizesForm(forms.ModelForm):
    model   = ClientSizes
    fields  = '__all__' 