# Generated by Django 3.2 on 2023-11-25 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storge', '0004_alter_clothrecord_typee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='الكمية'),
        ),
        migrations.AlterField(
            model_name='clothrecord',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='الكمية'),
        ),
    ]
