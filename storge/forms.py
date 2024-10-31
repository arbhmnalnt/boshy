from django import forms
from .models import *
from colorfield.fields import ColorField
from colorfield.widgets import ColorWidget

class ClothRecordForm(forms.ModelForm):
    class Meta:
        model = ClothRecord
        fields = '__all__'

class ClothForm(forms.ModelForm):
    name    =   forms.CharField(label="اسم القماش")
    amount    =   forms.CharField(label="الكمية")
    price    =   forms.CharField(label="سعر المتر")
    typee     =   forms.CharField(label="النوع")
    color = ColorField()
    
    class Meta:
        model = Cloth
        fields = ['name', 'amount', 'price', 'classs', 'typee', 'color']