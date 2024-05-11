# kazna/services.py
from .models import *
from client.models import Client
def record_money_in(classs,amount, master_invoice, details, clientt=None, remain=None):
    print(f"<<<< HERE 1 >>>>")

    if master_invoice:
        print(f"<<<< HERE 2 >>>>")
        Record.objects.create(classs=classs,amount=amount, kind='in', masterInvoice=master_invoice, details=details)        
     
    if master_invoice:
        print(f"<<<< HERE 3 >>>>")
        Record.objects.create(classs=classs,amount=amount, kind='in', masterInvoice=master_invoice, details=details)        
        if clientt:
            print(f"<<<< HERE 4 >>>>")
            DetailpayRecord.objects.create(paid=amount, remain=remain,classs=classs, masterInvoice=master_invoice, clientt=clientt)
    else:
        Record.objects.create(amount=amount, kind='in', masterInvoice=None, details=details)

    

def record_money_out(amount, master_invoice, details):
    if master_invoice:
        Record.objects.create(amount=amount, kind='out', masterInvoice=master_invoice, details=details)
    else:
        Record.objects.create(amount=amount, kind='out', masterInvoice=None, details=details)
