# Generated by Django 4.2 on 2024-07-29 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_debitorder_delete_debit'),
    ]

    operations = [
        migrations.AddField(
            model_name='debitorder',
            name='total',
            field=models.IntegerField(blank=True, null=True, verbose_name='المجموع'),
        ),
    ]
