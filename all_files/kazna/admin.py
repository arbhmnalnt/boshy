from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

class recordAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id', 'details')
    list_display    = ('id', 'details')

admin.site.register(Record, recordAdmin)

class DetailpayRecordAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id', 'clientMI_name')
    list_display    = ('id',)

admin.site.register(DetailpayRecord, DetailpayRecordAdmin)