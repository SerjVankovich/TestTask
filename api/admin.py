from django.contrib import admin
from .models import Printer, Check


# Register your models here.
@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'check_type', 'point_id')
    list_filter = ('name', 'api_key', 'check_type', 'point_id')


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('printer_id', 'type', 'status', 'pdf_file')
    list_filter = ['status', 'type', 'printer_id']
