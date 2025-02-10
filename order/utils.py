from order.models import *
def del_un_complete_order():
	# delete all uncompleted orders
	uncomplete_master_invoces_records = MasterInvoice.objects.filter(basicinvoiceinfo__isnull=True)

	count=uncomplete_master_invoces_records.count()
	print(f"uncomplete_master_invoces_records=> {uncomplete_master_invoces_records} \n Deleting {count} incomplete orders.")
	uncomplete_master_invoces_records.delete()
	return f"Deleted {count} incomplete orders."