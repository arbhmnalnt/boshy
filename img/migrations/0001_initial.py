# Generated by Django 3.2 on 2024-01-31 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=75, null=True, verbose_name='تصنيف الصورة')),
            ],
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=75, null=True, verbose_name='اسم الصورة')),
                ('kind', models.CharField(blank=True, choices=[('male', 'رجالى'), ('femal', 'حريمى')], default='male', max_length=10, null=True, verbose_name='نوع العميل')),
                ('file', models.FileField(blank=True, null=True, upload_to='imgs/')),
                ('sort', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='img.sort', verbose_name='تصنيف الصورة')),
            ],
        ),
    ]
