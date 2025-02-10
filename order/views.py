from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import *
from django.db.models import Q, Prefetch
from .forms import *

from client.models import ClientSizes
from client.forms import ClientSizesForm
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
import json
from kazna.services import *
from kazna.models import DetailpayRecord
from img.models import *
from django.utils.timezone import make_aware
from django.utils import timezone
from itertools import chain
from django.db.models import  Value, CharField, Sum
from datetime import datetime, timedelta
from .utils import del_un_complete_order


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
	elif statueVal == "5":
		val = "urgent"
	elif statueVal == "6":
		val = "late"
	else :
		val = "unknwon"

	print(f"statueVal => {statueVal}")
	print(f"val => {val}")

	masterInvoice = MasterInvoice.objects.get(pk=pk)
	basicInvoiceInfoRecords = basicInvoiceInfo.objects.filter(masterInvoice=masterInvoice)
	for record in basicInvoiceInfoRecords:
		record.statue = val  # Update the statue
		record.save()  # This will trigger the `updated_at` field to update

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
		master_invoice_pk = self.kwargs.get('pk')
		masterInvoice = MasterInvoice.objects.get(pk=master_invoice_pk)
		clientMI = masterInvoice.clientMI

		# Fetch client sizes
		client_sizes = ClientSizes.objects.get(clientS=clientMI)

		# Convert client sizes to a dictionary
		clientSizesDict = {
				"tall": client_sizes.tall,
				"kom": client_sizes.kom,
				"ktf": client_sizes.ktf,
				"sadr": client_sizes.sadr,
				"leaka": client_sizes.leaka,
				"kazna": client_sizes.kazna,
				"atak": client_sizes.atak,
		}

		# If the client is female, extract extra fields from `leaka`
		if clientMI.kindMale == "female":
				pass

				# Split leaka values
				leaka_values = client_sizes.leaka.split(":")  # Assuming "batn:hanch:sd:sh"

				# Ensure there are enough values before assigning
				if len(leaka_values) == 4:
						clientSizesDict.update({
								"batn": leaka_values[0] or "غير متوفر",
								"hanch": leaka_values[1] or "غير متوفر",
								"sd": leaka_values[2] or "غير متوفر",
								"sh": leaka_values[3] or "غير متوفر",
						})
				else:
						print(f"Warning: Unexpected leaka format -> {client_sizes.leaka}")


		# Add to context
		context["clientSizes"] = clientSizesDict
		context["masterInvoice"] = masterInvoice
		context["DetailedOrders"] = DetailedOrder.objects.filter(masterInvoice=masterInvoice)
		context["basicInfo"] = basicInvoiceInfo.objects.get(masterInvoice=masterInvoice)
		context["kaznaRecords"] = Record.objects.filter(masterInvoice=master_invoice_pk)

		return context

from datetime import datetime, timedelta


class needToBeDoneOrders(ListView):
	model = MasterInvoice
	template_name = 'order/orders_statue_List.html'
	context_object_name = 'masterInvoices'
	ordering = '-created_at'

	def get_queryset(self):
		today_date = timezone.now().date()
		three_days_ago = today_date - timedelta(days=3)
		today_date = timezone.now().date()
		queryset = MasterInvoice.objects.all().order_by('-basicinvoiceinfo__receve_date')

		# Filter by outdated status
		queryset = queryset.filter(
			Q(basicinvoiceinfo__statue='unknwon')|
			Q(basicinvoiceinfo__statue='sent'),
			basicinvoiceinfo__receve_date__gte=three_days_ago,
			basicinvoiceinfo__receve_date__lte=today_date
		).order_by('-basicinvoiceinfo__receve_date')

		return queryset



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

class dailyOrdersListView(ListView):
	model = MasterInvoice
	template_name = 'order/dailyOrdersListView.html'
	context_object_name = 'masterInvoices'
	ordering = '-created_at'

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset
	def get_context_data(self, **kwargs):
				context = super().get_context_data(**kwargs)
				from_date, to_date = get_date_range(self.request)
				kazna_in_records   = DetailpayRecord.objects.filter(created_at__range=(from_date, to_date)).select_related('masterInvoice').annotate(record_type=Value("kazna_in_records", output_field=CharField()))
				# Calculate the total amount for kazna_in_records
				kazna_in_total = kazna_in_records.aggregate(total_paid=Sum('paid'))['total_paid'] or 0
				kazna_out_records  = Expense.objects.filter(created_at__range=(from_date, to_date)).annotate(record_type=Value("kazna_out", output_field=CharField()))
				# Calculate the total amount for kazna_in_records
				kazna_out_total = kazna_out_records.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
				merged_records = sorted(
						chain(kazna_in_records, kazna_out_records),
						key=lambda record: record.created_at,
						reverse=True
				)

				context['records'] = merged_records
				context['from_date'] = from_date
				context['to_date'] = to_date
				context['kazna_in_total'] = kazna_in_total
				context['kazna_out_total'] = kazna_out_total
				context['remain'] = kazna_in_total - kazna_out_total
				return context

def cleanup_orders(request):
	str = del_un_complete_order()
	return JsonResponse({"message": str})

class ordersListView(ListView):

	model = MasterInvoice
	template_name = 'order/ordersList.html'
	context_object_name = 'masterInvoices'
	ordering = '-created_at'
	def get_queryset(self):
			queryset = super().get_queryset()

			# Initialize a Q object for flexible querying
			q_object = Q()

			# Handle search by client name or invoice number
			search_query = self.request.GET.get('q', '').strip()
			if search_query:
					if search_query.isdigit():
							# Search by invoice number
							q_object |= Q(counter=int(search_query))
					else:
							# Search by client name
							q_object |= Q(clientMI__name__icontains=search_query)

			# Handle filtering by specific search criteria
			search_by = self.request.GET.get('search_by')

			if search_by == "receve":
					from_date = self.request.GET.get('from')
					to_date = self.request.GET.get('to')
					if from_date and to_date:
							try:
									from_date_aware = make_aware(datetime.strptime(from_date, "%Y-%m-%d"))
									to_date_aware = make_aware(datetime.strptime(to_date, "%Y-%m-%d"))
									# Filter based on receve_date in basicInvoiceInfo
									basic_invoice_info_queryset = basicInvoiceInfo.objects.filter(
											receve_date__gte=from_date_aware,
											receve_date__lte=to_date_aware
									)
									# Filter MasterInvoice based on related basicInvoiceInfo
									q_object &= Q(id__in=basic_invoice_info_queryset.values('masterInvoice'))
							except ValueError:
									pass  # Handle invalid date format gracefully
			elif search_by == "created":
				from_date = self.request.GET.get('from')
				to_date = self.request.GET.get('to')
				if from_date and to_date:
						try:
								# Convert from_date and to_date into timezone-aware datetime objects
								from_date_aware = make_aware(datetime.strptime(from_date, "%Y-%m-%d"))
								to_date_aware = make_aware(datetime.strptime(to_date, "%Y-%m-%d"))
								# Filter by created_at date range
								q_object &= Q(created_at__gte=from_date_aware, created_at__lte=to_date_aware)

						except ValueError as e:
								# Handle invalid date format gracefully and log the error
								print(f"Invalid date format: {e}")
				else:
						# Log missing date range input
						print("Missing 'from' or 'to' date for created filter.")

			# Combine all filters
			queryset = queryset.filter(q_object)

		# Order results by created_at descending and return
			return queryset.order_by('-created_at')

from decimal import Decimal

class BasicOrderFormCreateView(FormView):
	form_class  = basicInvoiceInfoForm
	template_name   = 'order/basicOrderCreate_form.html'
	success_url = reverse_lazy('order:list')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		master_invoice_pk = self.kwargs.get('pk')
		master_invoice = MasterInvoice.objects.get(pk=master_invoice_pk)
		kwargs['client'] = master_invoice.clientMI  # Pass the client object
		return kwargs

	def get_initial(self):
		initial = super().get_initial()
		master_invoice_pk = self.kwargs.get('pk')
		master_invoice = MasterInvoice.objects.get(pk=master_invoice_pk)
		client = master_invoice.clientMI
		initial['masterInvoice'] = master_invoice
		initial['clientS'] = client
		# get related basicInvoiceInfo, if exists, populate form with its values, else set default values
		basic_info = master_invoice.basicinvoiceinfo_set.first()  # Assuming one-to-one or one-to-many, adjust if needed
		if basic_info:
			initial['paid'] = basic_info.paid
			initial['total'] = basic_info.total
			initial['remain'] = basic_info.remain
		else:
			# Provide default values if no related basicInvoiceInfo exists
			initial['paid'] = 0
			initial['total'] = 0
			initial['remain'] = 0

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

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		master_invoice_pk = self.kwargs.get('pk')
		master_invoice = MasterInvoice.objects.get(pk=master_invoice_pk)

		# Pass invoice type to form

		print(f"str(master_invoice.invoiceType) => {str(master_invoice.invoiceType)}")
		kwargs['invoice_type'] = str(master_invoice.invoiceType)
		return kwargs

	def get_initial(self):
		initial = super().get_initial()
		master_invoice_pk = self.kwargs.get('pk')
		master_invoice = MasterInvoice.objects.get(pk=master_invoice_pk)
		initial['masterInvoice'] = master_invoice
		orderType      = MasterInvoice.objects.get(pk=master_invoice_pk).invoiceType

		if 'رجالى' in str(orderType):
			imgs = Img.objects.filter(kind='male')
		elif 'حريمى' in str(orderType):
			imgs = Img.objects.filter(kind='female')
		initial['img'] = imgs
		return initial



		# Pass invoice type to form
		kwargs['invoice_type'] = str(master_invoice.invoiceType)
		return kwargs

	def get_context_data(self, **kwargs):
		print(f"kwargs =>  {kwargs}")
		context = super().get_context_data()
		master_invoice_pk = self.kwargs.get('pk')
		detailedOrders = DetailedOrder.objects.filter(masterInvoice__id=master_invoice_pk).order_by('-created_at')
		orderType      = MasterInvoice.objects.get(pk=master_invoice_pk).invoiceType

		if 'رجالى' in str(orderType):
			imgs = Img.objects.filter(kind='male')
		elif 'حريمى' in str(orderType):
			imgs = Img.objects.filter(kind='female')
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





def get_date_range(request):
		"""
		Extracts and processes 'date_from' and 'date_to' from the request.
		Returns a tuple (from_date_aware, to_date_aware).
		"""
		date_from = request.GET.get('date_from')
		date_to = request.GET.get('date_to')

		from_date_aware = None
		to_date_aware = None

		try:
				if date_from:
						# Parse and make the start date timezone-aware
						from_date_aware = make_aware(datetime.strptime(date_from, "%Y-%m-%d"))
				if date_to:
						# Parse and make the end date timezone-aware, inclusive of the entire day
						to_date_aware = make_aware(datetime.strptime(date_to, "%Y-%m-%d")) + timedelta(days=1, seconds=-1)
		except ValueError:
				# Handle invalid date formats gracefully (optional)
				pass

		return from_date_aware, to_date_aware