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
		def __init__(self, *args, invoice_type=None, **kwargs):

			super().__init__(*args, **kwargs)
			# Filter images based on invoice type
			print(f"invoice_type => {invoice_type}")

			if 'رجالى' in invoice_type:
				self.fields['img'].queryset = Img.objects.filter(kind='male')
			elif 'حريمى' in invoice_type:
				femal_imgs_count = Img.objects.filter(kind='female').count()
				print(f"male or female ==> {femal_imgs_count}")
				self.fields['img'].queryset = Img.objects.filter(kind='female')
			else:
					self.fields['img'].queryset = Img.objects.none()  # No images available


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

		def __init__(self, *args, **kwargs):
			client = kwargs.pop('client', None)  # Get client if passed from the view
			super().__init__(*args, **kwargs)
			if client:
				print(f"Client: {client.name}, Gender: {client.kindMale}")  # Debugging
			# Check if client is female
			if client and client.kindMale == 'female':
				# Add new female-specific fields
				self.fields['batn'] = forms.CharField(max_length=15, required=False, label="البطن")
				self.fields['hanch'] = forms.CharField(max_length=15, required=False, label="الهنش")
				self.fields['sd'] = forms.CharField(max_length=15, required=False, label="س/ص")
				self.fields['sh'] = forms.CharField(max_length=15, required=False, label="س/هـ")

				# Populate values from `leaka` field if editing an existing entry
				if 'leaka' in self.initial and self.initial['leaka']:
					try:
						batn, hanch, sd, sh = self.initial['leaka'].split(':')
						self.initial.update({'batn': batn, 'hanch': hanch, 'sd': sd, 'sh': sh})
					except ValueError:
						pass  # If leaka isn't in the expected format, ignore

		def clean(self):
			""" Override clean() to store female-specific fields in `leaka`. """
			cleaned_data = super().clean()
			client = cleaned_data.get('clientS')

			if client and client.kindMale == 'female':
				# Save female-specific sizes in `leaka`
				cleaned_data['leaka'] = f"{cleaned_data.get('batn', '')}:{cleaned_data.get('hanch', '')}:{cleaned_data.get('sd', '')}:{cleaned_data.get('sh', '')}"

			return cleaned_data


class DeliverdForm(forms.ModelForm):
		class Meta:
				model = Deliverd
				fields = '__all__'

class DebitForm(forms.ModelForm):
		class Meta:
				model  = DebitOrder
				fields  = ['MasterInvoice', 'paid', 'remain', 'total']
