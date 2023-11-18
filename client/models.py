from django.db import models
# Create your models here.
class TimeStampMixin(models.Model):
    is_deleted      = models.BooleanField (default=False, db_index=True)
    created_at      = models.DateTimeField(auto_now_add=True,null=True)
    updated_at      = models.DateTimeField(auto_now=True,null=True)

class Client(TimeStampMixin, models.Model):
    FName       = models.CharField(max_length=15, null=True, blank=True, verbose_name="الاسم الاول") # الاسم الاول
    SName       = models.CharField(max_length=15, null=True, blank=True, verbose_name="الاسم الثانى") # الاسم الثانى
    TName       = models.CharField(max_length=15, null=True, blank=True, verbose_name="الاسم الثالث") # الاسم الثالث
    LName       = models.CharField(max_length=15, null=True, blank=True, verbose_name="الاسم الرابع") # الاسم الرابع
    name        = models.CharField(max_length=50, null=True, blank=True, db_index=True,verbose_name="الاسم بالكامل") # الاسم بالكامل
    kindMale    = models.BooleanField(null=True, blank=True, verbose_name="نوع العميل : ذكر")
    page        = models.PositiveIntegerField(null=True, blank=True, verbose_name="صفحة رقم")
    phone       = models.CharField(max_length=11, null=True, blank=True, unique=True, db_index=True, verbose_name="رقم التليفون")
    address     = models.CharField(max_length=50, null=True, blank=True, verbose_name="العنوان")

    def save(self, *args, **kwargs):
        # Automatically populate the 'name' field with the concatenation of fName, SName, TName, and LName
        self.name = f"{self.FName} {self.SName} {self.TName} {self.LName}".strip()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name