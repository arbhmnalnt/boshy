# Generated by Django 3.2 on 2024-01-08 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_basicinvoiceinfo_receve_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailedorder',
            name='used',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='الكمية المستخدمة'),
        ),
    ]
