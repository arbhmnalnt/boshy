from django.shortcuts import render, get_object_or_404, redirect
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
from img.models import *
from django.utils.timezone import make_aware
from django.utils import timezone



@csrf_exempt
def change_details(request, order_id, masterInvoicePK):
    # Get the updated details from the request body
    updated_details = request.GET.get('details')
    print(f"order_id ===> {order_id}")
    DetailedOrder.objects.filter(pk=order_id).update(details=updated_details)
    # Process the updated details (e.g., save to the database)
    # Replace this with your actual logic to process the updated details
    print("Updated details:", updated_details)

    # # Redirect to a success page or reload the current page
    success_url = request.get_full_path()

class editDebitFormEditView(UpdateView):
    model           = DebitOrder
    form_class      = DebitForm
    template_name   = 'order/edit_debit.html'
    success_url = reverse_lazy('order:listDebit')

class debitListView(ListView):
    model = DebitOrder
    template_name = 'order/debit_List.html'
    context_object_name = 'orders'
    ordering = '-created_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        orders = self.get_queryset()
        order_pay_records = {}
        for order in orders:
            order_pay_records[order.pk] = DebitPay.objects.filter(DebitOrderRecord_id=order)
        context['order_pay_records'] = order_pay_records
        return context

def payDebitRecord(request, pk, paid):
    debitRecordPk = pk
    paid          = paid
    debitRecord   = DebitOrder.objects.get(pk=debitRecordPk)
    old_paid      = debitRecord.paid
    old_remain    = debitRecord.remain
    old_total     = debitRecord.total
    new_remain    = old_remain - paid
    new_paid      = old_paid + paid
    new_total     = new_remain + new_paid
    print(f"new_total: {new_total}, old_total: {old_total}")
    debitRecord.paid      = new_paid
    debitRecord.remain    = new_remain
    debitRecord.total     = new_total
    debitRecord.save()

    ### new debit record
    DebitPay.objects.create(DebitOrderRecord=debitRecord , paid=paid, remain = new_remain, total = new_total)
    success_url = reverse('order:listDebit')
    return HttpResponseRedirect(success_url)


def payDebit(request, pk):
    MasterInvoicePk = pk
    masterinvoicee = MasterInvoice.objects.get(pk=MasterInvoicePk)
    basic_info = basicInvoiceInfo.objects.filter(masterInvoice=masterinvoicee)[0]
    new_debitRecord =DebitOrder.objects.create(MasterInvoice=masterinvoicee, paid=basic_info.paid, remain = basic_info.remain)
    basic_info.remain = 0
    basic_info.save()
    DebitPay.objects.create(DebitOrderRecord=new_debitRecord , paid=basic_info.paid, remain = basic_info.remain, total = basic_info.total)
    success_url = reverse('order:list')
    return HttpResponseRedirect(success_url)


def DetailedOrderDelete(request, pk):
    masterInvoicePK = pk
    # delete details order
    old_DetailedOrder       = DetailedOrder.objects.filter(masterInvoice=masterInvoicePK).delete()
    print("done!")
    success_url = reverse('order:createDetails', kwargs={'pk': masterInvoicePK})
    return HttpResponseRedirect(success_url)

def dublicate(request,pk):
    masterInvoicePK = pk
    #  old data
    old_master_invoice      = MasterInvoice.objects.get(pk=masterInvoicePK)
    old_DetailedOrder       = DetailedOrder.objects.get(masterInvoice=old_master_invoice)
    old_basicInvoiceInfo    = basicInvoiceInfo.objects.get(masterInvoice=old_master_invoice)
    # create new records
    new_master_invoice = MasterInvoice.objects.create(
        invoiceType =old_master_invoice.invoiceType,
        clientMI    =old_master_invoice.clientMI,
        confirmed   =True
    )
    new_detail = DetailedOrder.objects.create(
        masterInvoice   =  new_master_invoice,
        name            =  old_DetailedOrder.name ,
        img             =  old_DetailedOrder.img,
        clothD          =  old_DetailedOrder.clothD ,
        used            =  old_DetailedOrder.used,
        details         =  old_DetailedOrder.details ,
    )

    new_basicInvoiceInfo = basicInvoiceInfo.objects.create(
        masterInvoice   =   new_master_invoice,
        total           =   old_basicInvoiceInfo.total,
        remain          =   old_basicInvoiceInfo.remain,
        receve_date     =   old_basicInvoiceInfo.receve_date,
        statue          =   'unknwon'
    )
    print("done!")
    success_url = reverse('order:list')
    return HttpResponseRedirect(success_url)

class DeliverdFormCreateView(CreateView):
    form_class  = DeliverdForm
    template_name   = 'order/deliverdCreate_form.html'
    success_url = reverse_lazy('order:list')

    def get_initial(self):
        initial = super().get_initial()
        master_invoice_pk = self.kwargs.get('pk')
        master_invoice = MasterInvoice.objects.get(pk=master_invoice_pk)
        basicInvoiceInfo_record = basicInvoiceInfo.objects.filter(masterInvoice=master_invoice).update(statue='delivered')
        initial['masterInvoice'] = master_invoice
        return initial

@csrf_exempt
def chabgeOrderStatue(request, pk):
    statueVal = request.POST.get('change_order_statue')
    if statueVal == "0" :
        val = "unknwon"
    elif statueVal == "1":
        val = "sent"
    elif statueVal == "2" :
        val = "done"
    elif statueVal == "3":
        val = "returned"
    elif statueVal == "4":
        val = "doneAgain"
    else :
        val = "unknwon"

    print(f"statueVal => {statueVal}")
    print(f"val => {val}")

    masterInvoice = MasterInvoice.objects.get(pk=pk)
    basicInvoiceInfoRecord = basicInvoiceInfo.objects.filter(masterInvoice=masterInvoice).update(statue=val)
    return JsonResponse({'message': 'done'})


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
        context["masterInvoice"]    = masterInvoice
        context["DetailedOrders"]   = DetailedOrder.objects.filter(masterInvoice=masterInvoice)
        context['basicInfo']        = basicInvoiceInfo.objects.get(masterInvoice=masterInvoice)
        context["clientSizes"]      = ClientSizes.objects.get(clientS=clientMI)
        context["kaznaRecords"]     = Record.objects.filter(masterInvoice=master_invoice_pk)
        return context

from datetime import datetime
class orderStatusListView(ListView):
    #TODO filter orders based on statues
    model = MasterInvoice
    template_name = 'order/orders_statue_List.html'
    context_object_name = 'masterInvoices'
    ordering = '-created_at'

    def get_queryset(self):
        order_status = self.request.GET.get('order_status')
        search_by = self.request.GET.get('search_by')
        from_date = self.request.GET.get('from')
        to_date = self.request.GET.get('to')
        today_date = timezone.now().date()

        queryset = MasterInvoice.objects.all().order_by('-basicinvoiceinfo__receve_date')

        # Filter by outdated status
        if order_status == "outdated":
            queryset = queryset.filter(
                ~Q(basicinvoiceinfo__statue='delivered'),
                ~Q(basicinvoiceinfo__statue='done'),
                basicinvoiceinfo__receve_date__lte=today_date
            ).order_by('-basicinvoiceinfo__receve_date')

        # Filter by receve date range
        if search_by == "receve" and from_date and to_date:
            from_date_aware = make_aware(datetime.strptime(from_date, "%Y-%m-%d"))
            to_date_aware = make_aware(datetime.strptime(to_date, "%Y-%m-%d"))
            queryset = queryset.filter(
                basicinvoiceinfo__receve_date__gte=from_date_aware,
                basicinvoiceinfo__receve_date__lte=to_date_aware
            ).order_by('-basicinvoiceinfo__receve_date')

        # Filter by specific order status if not already filtered by outdated status
        if order_status and order_status != "outdated":
            queryset = queryset.filter(basicinvoiceinfo__statue=order_status).order_by('-basicinvoiceinfo__receve_date')

        return queryset

class ordersListView(ListView):
    model = MasterInvoice
    template_name = 'order/ordersList.html'
    context_object_name = 'masterInvoices'
    ordering = '-created_at'

    def get_queryset(self):
        # MasterInvoice
        not_confirmed_orders = MasterInvoice.objects.filter(confirmed=False).delete()
        queryset = super().get_queryset()
        order_counter = len(queryset.all()) + 1
        # print(f'order_counter = > {order_counter}')
        # for ord in queryset:
        #     print(f"order_counter before = > {order_counter}")
        #     if ord.counter == None or ord.counter == 0:
        #         order_counter -= 1
        #         ord.counter = order_counter
        #         print(f'client id => {ord.id} // client counter =>>>>>>>>>>>{ord.counter}')
        #         ord.save()
        #     else:
        #         pass
        search_query = self.request.GET.get('q')
        search_by = self.request.GET.get('search_by')

        if search_query:
            q_object = Q(clientMI__name__icontains=search_query)
            q_object |= Q(invoiceType__icontains=search_query)
            if search_query.isdigit():
                q_object |= Q(counter=int(search_query))
            queryset = queryset.filter(q_object)
        elif search_by == "receve":
            from_date = self.request.GET.get('from')
            to_date = self.request.GET.get('to')

            # Ensure both from_date and to_date are provided
            if from_date and to_date:
                from_date_aware = make_aware(datetime.strptime(from_date, "%Y-%m-%d"))
                to_date_aware = make_aware(datetime.strptime(to_date, "%Y-%m-%d"))

                # Filter based on receve_date in basicInvoiceInfo
                basic_invoice_info_queryset = basicInvoiceInfo.objects.filter(receve_date__gte=from_date_aware, receve_date__lte=to_date_aware)

                # Get the related MasterInvoice records
                master_invoices = MasterInvoice.objects.filter(id__in=basic_invoice_info_queryset.values('masterInvoice')).distinct()

                return master_invoices

        return queryset.order_by('-created_at')

from decimal import Decimal

class BasicOrderFormCreateView(FormView):
    form_class  = basicInvoiceInfoForm
    template_name   = 'order/basicOrderCreate_form.html'
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
        masterInvoice.confirmed=True
        masterInvoice.save()
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
        classs = 'تفصيل - أول دفع'
        # record_money_in(classs,Decimal(str(paid)),master_invoice=masterInvoice, details=f"اجمالى المبلغ على العميل {masterInvoice.clientMI.name}  / {total}  / والمتبقى للدفع {remain}")
        client = masterInvoice.clientMI
        print(f'client == > {client.id} // {client.name}')
        record_money_in( classs, Decimal(str(paid)),master_invoice=masterInvoice, clientt=client, remain=remain,details=f"اجمالى المبلغ على العميل {masterInvoice.clientMI.name}  / {total}  / والمتبقى للدفع {remain}")

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

class DetailedOrderFormCreateView(CreateView):
    model           = DetailedOrder
    form_class       = DetailedOrderForm
    template_name   = 'order/detailedOrderCreate_form.html'

    def get_initial(self):
        initial = super().get_initial()
        master_invoice_pk = self.kwargs.get('pk')
        master_invoice = MasterInvoice.objects.get(pk=master_invoice_pk)
        initial['masterInvoice'] = master_invoice
        orderType      = MasterInvoice.objects.get(pk=master_invoice_pk).invoiceType

        if 'رجالى' in str(orderType):
            imgs = Img.objects.filter(kind='male')
        elif 'حريمى' in str(orderType):
            imgs = Img.objects.filter(kind='femal')
        initial['img'] = imgs
        return initial


    def get_context_data(self, **kwargs):
        print(f"kwargs =>  {kwargs}")
        context = super().get_context_data()
        master_invoice_pk = self.kwargs.get('pk')
        detailedOrders = DetailedOrder.objects.filter(masterInvoice__id=master_invoice_pk).order_by('-created_at')
        orderType      = MasterInvoice.objects.get(pk=master_invoice_pk).invoiceType

        if 'رجالى' in str(orderType):
            imgs = Img.objects.filter(kind='male')
        elif 'حريمى' in str(orderType):
            imgs = Img.objects.filter(kind='femal')
        else:
            imgs = ''

        context['imgsCount']            = imgs.count()
        context['imgs']                 = imgs
        context['detailedOrders']       = detailedOrders
        context['master_invoice_pk']    = master_invoice_pk
        context['instance']             = None

        return context
    def form_valid(self, form):
        response    = super().form_valid(form)
        # Save the form instance and get the ID
        masterInvoice = form.cleaned_data["masterInvoice"]
        clothId       = form.cleaned_data["clothD"]
        used          = Decimal(form.cleaned_data["used"])
        amountInStorge= Cloth.objects.get(pk=clothId).amount
        remain = amountInStorge - used
        self.request.session['second_step_complete']= True
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
        # print(f'invoiceType => {invoiceType}')
        self.request.session['first_step_complete'] = True

        print(f"self.request.session['first_step_complete'] => {self.request.session['first_step_complete']}")
        success_url = reverse('order:createDetails', kwargs={'pk': form_id})
        return HttpResponseRedirect(success_url)

##TO Do   make a function as first step order create is done already
##TO Do   make a function as second step order create is done already
##TO Do   make a function as third step order create is done already
##TO Do   function to check a;; 3 steps is done already or delete all the order related records

#-------------------- functions
## createMain_ConfirmStep()

## createDetails_ConfirmStep()
## createDetails_ConfirmStep()

## confirm order all info or delete all order related info
### Confirm_Order_or_delete_all_realted_order_info()