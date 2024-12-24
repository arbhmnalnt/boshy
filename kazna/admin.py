from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

class ExpenseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id', 'title', 'details')
    list_display    = ('id', 'title', 'details', 'created_at')

class recordAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id', 'details')
    list_display    = ('id', 'details', 'created_at')

admin.site.register(Record, recordAdmin)

class DetailpayRecordAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id', 'clientMI_name')
    list_display    = ('id', 'created_at')

admin.site.register(DetailpayRecord, DetailpayRecordAdmin)

class DetailpayRecordAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id',)
    list_display    = ('id', 'created_at')

admin.site.register(Expense, ExpenseAdmin)

