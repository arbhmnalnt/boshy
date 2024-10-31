from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class MasterInvoiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id',)
    list_display    = ('id',)
admin.site.register(MasterInvoice, MasterInvoiceAdmin)

class DetailedOrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id',)
    list_display    = ('id',)
admin.site.register(DetailedOrder, DetailedOrderAdmin)

class basicInvoiceInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id',)
    list_display    = ('id',)

admin.site.register(basicInvoiceInfo, basicInvoiceInfoAdmin)

class PayDebitAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('id',)
    list_display  = ('id',)
  
admin.site.register(DebitOrder, PayDebitAdmin)

class DebitPayAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ('id',)
    list_display  = ('id',)

admin.site.register(DebitPay, DebitPayAdmin)


class DeliverdAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id',)
    list_display    = ('id',)

admin.site.register(Deliverd, DeliverdAdmin)
