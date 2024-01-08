from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView 
from .models import *
from django.db.models import Q
from .forms import *
from client.models import ClientSizes
from client.forms import ClientSizesForm
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
import json
from kazna.services import *

@csrf_exempt
def getClothStorgedAmount(request):
    if request.method == "POST":
        data                    = json.loads(request.body.decode('utf-8'))
        print(f"data =====================> {data}")
        cloth_id                = data.get('clothId', 'No data received.')
        print(f"cloth_id =====================> {cloth_id}")
        cloth_storged_amount    = Cloth.objects.get(pk=cloth_id).amount
    
        response_data = {
            'status': 'success',
            'cloth_storged_amount': cloth_storged_amount
        }

    return JsonResponse(response_data)

class ordersDetailView(DetailView):
    model               =   MasterInvoice
    template_name       =   'order/ordersDetailView.html'
    context_object_name =   'masterInvoices'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        master_invoice_pk   = self.kwargs.get('pk')
        masterInvoice       = MasterInvoice.objects.get(pk=master_invoice_pk)
        clientMI            = masterInvoice.clientMI
        context["masterInvoice"]   = masterInvoice
        context["DetailedOrders"]   = DetailedOrder.objects.filter(masterInvoice=masterInvoice)
        context["clientSizes"]   = ClientSizes.objects.get(clientS=clientMI)
        return context

class ordersListView(ListView):
    model               =   MasterInvoice
    template_name       =   'order/ordersList.html'
    context_object_name =   'masterInvoices'
    ordering            =   '-created_at'
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            q_object = Q(clientMI__name__icontains=search_query)
            q_object |= Q(invoiceType__icontains=search_query)
            if search_query.isdigit():
                q_object |= Q(counter=int(search_query))

            queryset = queryset.filter(q_object)

        queryset = queryset.order_by('-created_at')

        return queryset
    
from decimal import Decimal

class BasicOrderFormCreateView(FormView):
    form_class  = basicInvoiceInfoForm
    template_name   = 'order/basicOrderCreate_form.html'
#    success_url    = reverse('order:list')
    success_url = reverse_lazy('order:list')

    def get_initial(self):
        initial = super().get_initial()
        master_invoice_pk = self.kwargs.get('pk')
        master_invoice = MasterInvoice.objects.get(pk=master_invoice_pk)
        client = master_invoice.clientMI
        initial['masterInvoice'] = master_invoice
        initial['clientS'] = client

        clientSizes = ClientSizes.objects.filter(clientS=client).count()
        if clientSizes > 0 :
            clientSizes = ClientSizes.objects.filter(clientS=client).first()
            # set sizes 
            initial['tall'] = clientSizes.tall
            initial['kom'] = clientSizes.kom
            initial['ktf'] = clientSizes.ktf
            initial['sadr'] = clientSizes.sadr
            initial['leaka'] = clientSizes.leaka
            initial['kazna'] = clientSizes.kazna
            initial['atak'] = clientSizes.atak
        else:
            pass
        return initial
    def form_valid(self, form):
        response    = super().form_valid(form)
        # make record save to basicInvoiceInfo,

        masterInvoice = form.cleaned_data["masterInvoice"]
        total       = form.cleaned_data["total"]
        paid        = form.cleaned_data["paid"]
        remain      = form.cleaned_data["remain"]
        receve_date = form.cleaned_data["receve_date"]
        basicInvoiceInfo.objects.update_or_create(
            masterInvoice= masterInvoice,
            defaults={
                'total': total,
                'paid': paid,
                'remain':remain,
                'receve_date':receve_date
            }
        )

        record_money_in(Decimal(str(paid)),masterInvoice=masterInvoice, details=f"اجمالى المبلغ على العميل {masterInvoice.clientMI.name}  / {total}  / والمتبقى للدفع {remain}")

        tall  = form.cleaned_data["tall"]
        kom   = form.cleaned_data["kom"]
        ktf   = form.cleaned_data["ktf"] 
        sadr  = form.cleaned_data["sadr"] 
        leaka = form.cleaned_data["leaka"]
        kazna = form.cleaned_data["kazna"]
        atak  = form.cleaned_data["atak"] 
        client = form.cleaned_data["clientS"]

        client_id = client.id
        ClientSizes.objects.update_or_create(
            clientS=client,  # Provide the clientS foreign key
            defaults={
                'tall': tall,
                'kom': kom,
                'ktf': ktf,
                'sadr': sadr,
                'leaka': leaka,
                'kazna': kazna,
                'atak': atak,
            }
        )

        success_url = reverse('order:list')
        return HttpResponseRedirect(success_url)
    
from decimal import Decimal

class DetailedOrderFormCreateView(CreateView):
    model           = DetailedOrder
    form_class       = DetailedOrderForm
    template_name   = 'order/detailedOrderCreate_form.html'

    def get_initial(self):
        initial = super().get_initial()
        master_invoice_pk = self.kwargs.get('pk')
        master_invoice = MasterInvoice.objects.get(pk=master_invoice_pk)
        initial['masterInvoice'] = master_invoice
        return initial

    
    def get_context_data(self, **kwargs):
        print(f"kwargs =>  {kwargs}")
        context = super().get_context_data()
        master_invoice_pk = self.kwargs.get('pk')
        detailedOrders = DetailedOrder.objects.filter(masterInvoice__id=master_invoice_pk).order_by('-created_at')
        context['detailedOrders'] = detailedOrders
        context['master_invoice_pk'] = master_invoice_pk
        context['instance'] = None
        
        return context
    def form_valid(self, form):
        response    = super().form_valid(form)
        # Save the form instance and get the ID
        masterInvoice = form.cleaned_data["masterInvoice"]
        clothId       = form.cleaned_data["clothD"]
        used          = Decimal(form.cleaned_data["used"])
        amountInStorge= Cloth.objects.get(pk=clothId).amount
        remain = amountInStorge - used
        print(f"remain =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {remain}")
        Cloth.objects.filter(pk=clothId).update(amount=remain)


        print(f'masterInvoice => {masterInvoice}')
        success_url = reverse('order:createDetails', kwargs={'pk': masterInvoice.id})
        return HttpResponseRedirect(success_url)

class MasterInvoiceFormCreateView(CreateView):
    model   = MasterInvoice
    form_class = MasterInvoiceForm
    template_name = 'order/masterInvoiceCreate_form.html'
    def form_valid(self, form):
        # Save the form instance and get the ID
        response    = super().form_valid(form)
        form_id     = self.object.id
        invoiceType = form.cleaned_data["invoiceType"]
        print(f'invoiceType => {invoiceType}')
        success_url = reverse('order:createDetails', kwargs={'pk': form_id})
        return HttpResponseRedirect(success_url)