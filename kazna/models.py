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
    amount          = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="المبلغ")
    details         = models.TextField(null=True, blank=True, verbose_name="التفصيل")
