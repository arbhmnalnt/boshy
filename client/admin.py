from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class ClientAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields   = ('id', 'name', 'address', 'phone')
    list_filter     = ('id', 'name', 'address')
    list_display    = ('id', 'name', 'page', 'kindMale', 'address', 'phone', 'created_at')

admin.site.register(Client, ClientAdmin)
