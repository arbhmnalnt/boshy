from django.db import models
from django.db.models import Max

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db import connection

# Create your models here.
class TimeStampMixin(models.Model):
    created_at      = models.DateTimeField(auto_now_add=True,null=True)
    updated_at      = models.DateTimeField(auto_now=True,null=True)
    is_deleted      = models.BooleanField(default=False)


class Client(TimeStampMixin, models.Model):
    GENDER_CHOICES = [
        ('male', 'رجالى'),
        ('female', 'حريمى'),
    ]
    counter     = models.PositiveIntegerField(default=0, verbose_name="رقم العميل")
    FName       = models.CharField(max_length=15, null=True, blank=True, verbose_name="الاسم الاول") # الاسم الاول
    SName       = models.CharField(max_length=15, null=True, blank=True, verbose_name="الاسم الثانى") # الاسم الثانى
    TName       = models.CharField(max_length=15, null=True, blank=True, verbose_name="الاسم الثالث") # الاسم الثالث
    LName       = models.CharField(max_length=15, null=True, blank=True, verbose_name="الاسم الرابع") # الاسم الرابع
    name        = models.CharField(max_length=60, null=True, blank=True, db_index=True,verbose_name="الاسم بالكامل") # الاسم بالكامل
    kindMale    = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True, verbose_name="نوع العميل", default="male" )
    book        = models.CharField(max_length=50, null=True, blank=True, verbose_name="اسم الدفتر")
    page        = models.IntegerField(null=True, blank=True, verbose_name="صفحة رقم")
    phone       = models.CharField(max_length=50, null=True, blank=True, db_index=True, verbose_name="رقم التليفون")
    address     = models.CharField(max_length=50, null=True, blank=True, verbose_name="العنوان")

    def __str__(self):
        return f"{self.name} ({str(self.id)}) "

    def save(self, *args, **kwargs):
        # Automatically populate the 'name' field with the concatenation of fName, SName, TName, and LName
        self.name = f"{self.FName} {self.SName} {self.TName} {self.LName}".strip()
        super().save(*args, **kwargs)

@receiver(post_save, sender=Client)
def update_counter(sender, instance, created, **kwargs):
    if created:
        # Get the maximum existing counter value
        max_counter = Client.objects.aggregate(Max('counter'))['counter__max']
        if max_counter is not None:
            # Increment the counter for the newly created instance
            instance.counter = max_counter + 1
        else:
            # If there are no existing records, set the counter to 1
            instance.counter = 1
        instance.save()

@receiver(pre_delete, sender=Client)
def decrement_counter(sender, instance, **kwargs):
    # Decrement counter for deleted instance
    Client.objects.filter(id__gt=instance.id).update(counter=models.F('counter') - 1)


class CounterField(models.PositiveIntegerField):
    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if add:
            last_client = Client.objects.last()
            if last_client:
                value = last_client.counter + 1
            else:
                value = 1
        return value

class ClientSizes(TimeStampMixin, models.Model):
    clientS  = models.ForeignKey('Client', related_name='client', on_delete=models.CASCADE)
    tall    = models.CharField(max_length=5, null=True, blank=True, verbose_name="الطول") # الطول
    kom     = models.CharField(max_length=5, null=True, blank=True, verbose_name="الكم") # الكم
    ktf     = models.CharField(max_length=5, null=True, blank=True, verbose_name="الكتف") # الكتف
    sadr    = models.CharField(max_length=5, null=True, blank=True, verbose_name="الصدر") # الصدر
    leaka   = models.CharField(max_length=5, null=True, blank=True, verbose_name="اللياقه") # اللياقه
    kazna   = models.CharField(max_length=5, null=True, blank=True, verbose_name="الخزنه") # الخزنه
    t       = models.CharField(max_length=5, null=True, blank=True, verbose_name="دوران الرقبه")
    atak    = models.CharField(max_length=5, null=True, blank=True, verbose_name="الأتك") # الأتك

    def __str__(self):
        return self.clientS.name