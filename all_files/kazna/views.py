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

@csrf_exempt
def pay(request, pk, paid):
    paid_user = paid
    masterInvoice = MasterInvoice.objects.get(pk=pk)
    
    total = basicInvoiceInfo.objects.get(masterInvoice=masterInvoice).total
    paid = basicInvoiceInfo.objects.get(masterInvoice=masterInvoice).paid
    remain = total - (paid_user + paid)
    paid   =  paid_user + paid
    basicInvoiceInfo_records = basicInvoiceInfo.objects.filter(masterInvoice=masterInvoice).update(remain=remain, paid=paid)
    classs = 'استكمال مبلغ'
    record_money_in( classs, Decimal(str(paid)),master_invoice=masterInvoice, details=f"اجمالى المبلغ على العميل {masterInvoice.clientMI.name}  / {total}  / والمتبقى للدفع {remain}")
    return redirect('order:list')



class recordsListView(ListView):
    model               =   Record
    template_name       =   'kazna/recordsList.html'
    context_object_name =   'records'
    ordering            =   '-created_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        from_date = self.request.GET.get('from')
        to_date = self.request.GET.get('to')

        if search_query:
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

        # Calculate the difference for each record
        # for record in context['records']:
        #     record.difference = record.masterInvoice.basicinvoiceinfo_set.aggregate(Sum('total'))['total__sum'] - record.amount

        return context