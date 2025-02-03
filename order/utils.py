from order.models import *
def del_un_complete_order():
	# delete all uncompleted orders
	uncomplete_master_invoces_records = MasterInvoice.objects.filter(detailedorder__isnull=True)
	count=uncomplete_master_invoces_records.count()
	uncomplete_master_invoces_records.delete()
	return f"Deleted {count} incomplete orders."