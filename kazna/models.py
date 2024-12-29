from django.db import models
from client.models import TimeStampMixin, Client
from order.models import MasterInvoice


class Record (TimeStampMixin,models.Model):
    typee = [
        ('in'   ,   'وارد'),
        ('out'  ,   'صادر')
    ]
    kind            = models.CharField(max_length=35, choices=typee, null=True, blank=True, verbose_name="نوع المبلغ", default="in")
    masterInvoice   = models.ForeignKey(MasterInvoice, on_delete=models.CASCADE, verbose_name="الفاتورة")
    amount          = models.IntegerField(null=True, blank=True, verbose_name="المبلغ")
    classs           = models.CharField(max_length=35, null=True, blank=True, verbose_name="تصنيف الدفع")
    details         = models.TextField(null=True, blank=True, verbose_name="التفصيل")

class DetailpayRecord(TimeStampMixin,models.Model):
    clientt          = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="العميل")
    masterInvoice   = models.ForeignKey(MasterInvoice, on_delete=models.CASCADE, verbose_name="الفاتورة")
    classs           = models.CharField(max_length=35, null=True, blank=True, verbose_name="تصنيف الدفع", default='-')
    paid              = models.IntegerField(null=True, blank=True, verbose_name="المبلغ المدفوع")
    remain              = models.IntegerField(null=True, blank=True, verbose_name="المبلغ المتبقى")


class Expense(TimeStampMixin,models.Model):
    title           = models.CharField(max_length=50, null=True, blank=True, verbose_name="مسمى الدفع")
    amount          = models.IntegerField(null=True, blank=True, verbose_name="المبلغ")
    details         = models.TextField(null=True, blank=True, verbose_name="التفصيل")
