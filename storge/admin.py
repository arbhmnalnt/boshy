from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin



class ClasssAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display    = ('id', 'name')
admin.site.register(Classs,ClasssAdmin)

class ClothAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id', 'name', 'amount', 'classs__name', 'typee')
    list_filter     = ('classs__name', 'typee')
    list_display    = ('id', 'name', 'amount', 'typee', 'color')
admin.site.register(Cloth, ClothAdmin)

class ClothRecordAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display    = ('id', 'get_name', 'amount')

    def get_name(request,self):
        return self.clothh.name
    
admin.site.register(ClothRecord,ClothRecordAdmin)