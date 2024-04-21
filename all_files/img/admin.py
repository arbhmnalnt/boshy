from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

class ImgAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id','name')
    list_display    = ('id','sort')

admin.site.register(Img, ImgAdmin)

class SortAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id','name')
    list_display    = ('id','name')

admin.site.register(Sort, SortAdmin)
