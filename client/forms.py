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