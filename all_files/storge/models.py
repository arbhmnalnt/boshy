from django.db import models
from client.models import TimeStampMixin
from colorfield.fields import ColorField
from simple_history.models import HistoricalRecords


class Classs(models.Model):
    name       = models.CharField(max_length=50, null=True, blank=True, verbose_name="اسم التصنيف")
    def __str__(self):
        return self.name


class Cloth(TimeStampMixin, models.Model):
    name       = models.CharField(max_length=50, null=True, blank=True, verbose_name="اسم القماش") 
    amount     = models.DecimalField(max_digits=9,decimal_places=2, null=True, blank=True, verbose_name="الكمية") 
    price      = models.CharField(max_length=5, null=True, blank=True, verbose_name="سعر المتر") 
    classs     = models.ForeignKey('Classs', on_delete=models.CASCADE, null=True, blank=True, verbose_name="التصنيف")
    typee      = models.CharField(max_length=50, null=True, blank=True, db_index=True,verbose_name="النوع") 
    color      = ColorField(verbose_name="لون القماش", null=True, blank=True)
    history    = HistoricalRecords()
        
    def __str__(self):
        return self.name
    
class ClothRecord(TimeStampMixin, models.Model):
    Cloth_CHOICES = [
        ('inside', 'وارد'),
        ('outside', 'صادر'),
    ]
    clothh     = models.ForeignKey('Cloth', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="القماش")
    amount     = models.DecimalField(max_digits=5,decimal_places=2, null=True, blank=True, verbose_name="الكمية")
    typee      = models.CharField(max_length=10, choices=Cloth_CHOICES, null=True, blank=True, verbose_name="نوع السجل", default="inside")

    def __str__(self):
        return self.clothh.name
