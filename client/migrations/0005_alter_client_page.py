# Generated by Django 3.2 on 2023-11-18 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_auto_20231118_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='page',
            field=models.IntegerField(blank=True, null=True, verbose_name='صفحة رقم'),
        ),
    ]
