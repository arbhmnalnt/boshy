# kazna/services.py
from .models import Record

def record_money_in(amount, master_invoice, details):
    if master_invoice:
        Record.objects.create(amount=amount, kind='in', masterInvoice=master_invoice, details=details)
    else:
        Record.objects.create(amount=amount, kind='in', masterInvoice=None, details=details)

def record_money_out(amount, master_invoice, details):
    if master_invoice:
        Record.objects.create(amount=amount, kind='out', masterInvoice=master_invoice, details=details)
    else:
        Record.objects.create(amount=amount, kind='out', masterInvoice=None, details=details)
