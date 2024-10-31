from django import forms
from .models import *


class ClientForm(forms.ModelForm):
    FName    =   forms.CharField(label="الاسم الاول", widget=forms.TextInput(attrs={'class': 'form-control'}))
    SName    =   forms.CharField(label="الاسم الثانى", widget=forms.TextInput(attrs={'class': 'form-control'}))
    TName    =   forms.CharField(label="الاسم الثالث", widget=forms.TextInput(attrs={'class': 'form-control'}))
    LName    =   forms.CharField(label="الاسم الرابع", widget=forms.TextInput(attrs={'class': 'form-control'}))
    book     =   forms.CharField(label="الدفتر", widget=forms.TextInput(attrs={'class': 'form-control'}))
    page     =   forms.CharField(label="رقم الصفحة", widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone    =   forms.CharField(label="رقم التليفون", widget=forms.TextInput(attrs={'class': 'form-control'}))
    address  =   forms.CharField(label="العنوان ", widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    kindMale = forms.ChoiceField(
        label="نوع العميل", 
        choices=Client.GENDER_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

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