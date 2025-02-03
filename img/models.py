from django.db import models

class Sort(models.Model):
    name          = models.CharField(max_length=75, null=True, blank=True, verbose_name="تصنيف الصورة")

    def __str__(self):
        return self.name

class Img (models.Model):
    name          = models.CharField(max_length=75, null=True, blank=True, verbose_name="اسم الصورة")
    GENDER_CHOICES = [
        ('male'   ,   'رجالى'),
        ('female'  ,   'حريمى')
    ]
    kind            = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True, verbose_name="نوع العميل", default="male" )
    sort            = models.ForeignKey("Sort", verbose_name="تصنيف الصورة", on_delete=models.CASCADE, null=True, blank=True)
    file            = models.FileField(upload_to=f'uploade_imgs/', max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name