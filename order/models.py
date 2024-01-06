from django.db import models
from client.models import TimeStampMixin, Client
from storge.models import Cloth
from django.urls import reverse

# Create your models here.


class MasterInvoice( TimeStampMixin,models.Model):
    counter = models.PositiveIntegerField(default=1, editable=False)
    invoiceType = [
        ('قماش الدكان-رجالى', 'قماش الدكان-رجالى'),
        ('قماش الدكان-حريمى', 'قماش الدكان-حريمى'),
        ('قماش خارجى-رجالى', 'قماش خارجى-رجالى'),
        ('قماش خارجى-حريمى', 'قماش خارجى-حريمى'),
        ('بيع قماش', 'بيع قماش'),
    ]
    clientMI    = models.ForeignKey(Client, related_name='master_invoices', on_delete=models.CASCADE, verbose_name="العميل")
    invoiceType = models.CharField(max_length=35, choices=invoiceType, null=True, blank=True, verbose_name="نوع الطلب", default="قماش الدكان-رجالى")

    def save(self, *args, **kwargs):
        # Check if the instance is being saved for the first time
        if not self.id:
            # Query the maximum counter value in the table
            max_counter = MasterInvoice.objects.all().aggregate(models.Max('counter'))['counter__max']

            # Increment the counter value
            self.counter = max_counter + 1 if max_counter else 1

        super(MasterInvoice, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('order:createDetails', kwargs={'pk': self.pk})
    
    def __str__(self):
        return f" الفاتورة رقم ({self.id})"


# ==========  tables for many orders in on Invoice
class DetailedOrder (TimeStampMixin,models.Model):
    masterInvoice   = models.ForeignKey(MasterInvoice, on_delete=models.CASCADE, verbose_name="الفاتورة")
    name            = models.CharField(max_length=90, null=True, blank=True, verbose_name="اسم الطلب") 
    clothD          = models.ForeignKey(Cloth, on_delete=models.CASCADE, verbose_name="القماش")
    used            = models.DecimalField(max_digits=3, decimal_places=2,null=True, blank=True, verbose_name="الكمية المستخدمة")
    details         = models.TextField(null=True, blank=True, verbose_name="التفصيل")

    def get_absolute_url(self):
            return reverse('order:createDetails', kwargs={'pk': self.pk})

# ==========  tables for basics infos 
class basicInvoiceInfo(TimeStampMixin,models.Model):
    masterInvoice   = models.ForeignKey(MasterInvoice, on_delete=models.CASCADE, verbose_name="الفاتورة")
    total           = models.IntegerField(null=True, blank=True, verbose_name="المبلغ الإجمالى")
    paid            = models.IntegerField(null=True, blank=True, verbose_name="المبلغ المدفوع")
    remain          = models.IntegerField(null=True, blank=True, verbose_name="المبلغ المتبقى")
    receve_date     = models.DateField(blank=True, null=True)
