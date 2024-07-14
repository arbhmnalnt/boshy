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
from django.utils.timezone import make_aware
from datetime import *


class ExpenseListView(ListView):
    model               =   Expense
    template_name       =   'kazna/expenseList.html'
    context_object_name =   'records'
    ordering            =   '-created_at'



class ExpenseFormcreatView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'kazna/ExpenseForm.html'
    success_url = reverse_lazy('kazna:expense_list')


@csrf_exempt
def pay(request, pk, paid):
    paid_user = paid
    masterInvoice = MasterInvoice.objects.get(pk=pk)
    client = masterInvoice.clientMI
    total = basicInvoiceInfo.objects.get(masterInvoice=masterInvoice).total
    paid = basicInvoiceInfo.objects.get(masterInvoice=masterInvoice).paid
    remain = total - (paid_user + paid)
    paid   =  paid_user + paid
    basicInvoiceInfo_records = basicInvoiceInfo.objects.filter(masterInvoice=masterInvoice).update(remain=remain, paid=paid)
    classs = 'استكمال مبلغ'
    print(f">>>> >>>>>   starting detail pay record recording ")
    record_money_in( classs, Decimal(str(paid_user)),master_invoice=masterInvoice, clientt=client, remain=remain,details=f"اجمالى المبلغ على العميل {masterInvoice.clientMI.name}  / {total}  / والمتبقى للدفع {remain}")
    print(f" ending detail pay record recording <<<<<")
    # client 
    
    return redirect('order:list')

class oldRecordsListView(ListView):
    model               =   Record
    template_name       =   'kazna/oldRecordsList.html'
    context_object_name =   'records'
    ordering            =   '-created_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        from_date = self.request.GET.get('from')
        to_date = self.request.GET.get('to')
        
        if search_query and from_date and to_date :
            from_date_aware = make_aware(datetime.strptime(from_date, "%Y-%m-%d"))
            to_date_aware = make_aware(datetime.strptime(to_date, "%Y-%m-%d")) 
            q_object = Q(masterInvoice__clientMI__name__icontains=search_query , created_at__gte=from_date_aware, created_at__lte=to_date_aware)
            queryset = queryset.filter(q_object)
        elif search_query:
            q_object = Q(masterInvoice__clientMI__name__icontains=search_query)
            q_object |= Q(masterInvoice__invoiceType__icontains=search_query)
            if search_query.isdigit():
                q_object |= Q(masterInvoice__counter=int(search_query))
            queryset = queryset.filter(q_object)
        elif from_date and to_date:
            from_date_aware = make_aware(datetime.strptime(from_date, "%Y-%m-%d"))
            to_date_aware = make_aware(datetime.strptime(to_date, "%Y-%m-%d")) 
            q_object = Q(created_at__gte=from_date_aware, created_at__lte=to_date_aware)
            queryset = queryset.filter(q_object)

        return queryset.order_by('-created_at')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     records = context['records']
    #     total_paid = sum(record.paid for record in records)
    #     context['total_paid'] = total_paid
    #     # Calculate the difference for each record
    #     # for record in context['records']:
    #     #     record.difference = record.masterInvoice.basicinvoiceinfo_set.aggregate(Sum('total'))['total__sum'] - record.amount

    #     return context
    
class recordsListView(ListView):
    model               =   DetailpayRecord
    template_name       =   'kazna/recordsList.html'
    context_object_name =   'records'
    ordering            =   '-created_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        from_date = self.request.GET.get('from')
        to_date = self.request.GET.get('to')
        
        if search_query and from_date and to_date :
            from_date_aware = make_aware(datetime.strptime(from_date, "%Y-%m-%d"))
            to_date_aware = make_aware(datetime.strptime(to_date, "%Y-%m-%d")) 
            q_object = Q(masterInvoice__clientMI__name__icontains=search_query , created_at__gte=from_date_aware, created_at__lte=to_date_aware)
            queryset = queryset.filter(q_object)
        elif search_query:
            q_object = Q(masterInvoice__clientMI__name__icontains=search_query)
            q_object |= Q(masterInvoice__invoiceType__icontains=search_query)
            if search_query.isdigit():
                q_object |= Q(masterInvoice__counter=int(search_query))
            queryset = queryset.filter(q_object)
        elif from_date and to_date:
            from_date_aware = make_aware(datetime.strptime(from_date, "%Y-%m-%d"))
            to_date_aware = make_aware(datetime.strptime(to_date, "%Y-%m-%d")) 
            q_object = Q(created_at__gte=from_date_aware, created_at__lte=to_date_aware)
            queryset = queryset.filter(q_object)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        records = context['records']
        total_paid = sum(record.paid for record in records)
        context['total_paid'] = total_paid
        # Calculate the difference for each record
        # for record in context['records']:
        #     record.difference = record.masterInvoice.basicinvoiceinfo_set.aggregate(Sum('total'))['total__sum'] - record.amount

        return context