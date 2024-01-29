from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView 
from .models import *
from django.db.models import Q
# from .forms import *
from client.models import ClientSizes
from client.forms import ClientSizesForm
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
import json
from kazna.services import *
from .forms import *
from order.models import *
# Create your views here.
from decimal import Decimal
from django.db.models import Sum



@csrf_exempt
def pay(request, pk, paid):
    paid_user = paid
    masterInvoice = MasterInvoice.objects.get(pk=pk)
    
    total = basicInvoiceInfo.objects.get(masterInvoice=masterInvoice).total
    paid = basicInvoiceInfo.objects.get(masterInvoice=masterInvoice).paid
    remain = total - (paid_user + paid)
    paid   =  paid_user + paid
    basicInvoiceInfo_records = basicInvoiceInfo.objects.filter(masterInvoice=masterInvoice).update(remain=remain, paid=paid)
    record_money_in(Decimal(str(paid)),master_invoice=masterInvoice, details=f"اجمالى المبلغ على العميل {masterInvoice.clientMI.name}  / {total}  / والمتبقى للدفع {remain}")
    return redirect('order:list')



class recordsListView(ListView):
    model               =   Record
    template_name       =   'kazna/recordsList.html'
    context_object_name =   'records'
    ordering            =   '-created_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate the difference for each record
        for record in context['records']:
            record.difference = record.masterInvoice.basicinvoiceinfo_set.aggregate(Sum('total'))['total__sum'] - record.amount

        return context