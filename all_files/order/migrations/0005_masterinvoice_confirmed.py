# Generated by Django 5.0.3 on 2024-04-26 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_remove_masterinvoice_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterinvoice',
            name='confirmed',
            field=models.BooleanField(default=True),
        ),
    ]
