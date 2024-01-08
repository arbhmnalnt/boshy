# kazna/services.py
from .models import Record

def record_money_in(amount, master_invoice=None, details=None):
    if master_invoice:
        Record.objects.create(amount, kind='in', masterInvoice=master_invoice, details=details)
    else:
        Record.objects.create(amount, kind='in', details=details)

def record_money_out(amount, master_invoice=None, details=None):
    if master_invoice:
        Record.objects.create(amount, kind='out', masterInvoice=master_invoice, details=details)
    else:
        Record.objects.create(amount, kind='out', details=details)