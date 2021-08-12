# Generated by Django 3.2.2 on 2021-08-12 06:55

import datetime
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('E', 'Estimate'), ('B', 'Booked'), ('A', 'Awaiting Payment (Show Concluded)'), ('C', 'Closed')], default='E', max_length=1)),
                ('signed_estimate', models.FileField(blank=True, null=True, upload_to='estimates')),
                ('notes', tinymce.models.HTMLField(blank=True, help_text='These notes will appear on the estimate to be signed by the client.', null=True)),
                ('payment_due', models.DateField(blank=True, null=True)),
                ('paid', models.DateField(blank=True, null=True)),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7, null=True)),
                ('fees_amt', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7, null=True)),
                ('adjustments', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, null=True)),
                ('total_amt', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=7, null=True)),
                ('billing_contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='client.orgcontact')),
            ],
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_in', models.DateTimeField()),
                ('time_out', models.DateTimeField(blank=True, null=True)),
                ('total_time', models.DurationField(default=datetime.timedelta(0))),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('processed', models.BooleanField(default=False)),
                ('contested', models.BooleanField(default=False)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='PayPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('payday', models.DateField()),
                ('submitted', models.BooleanField(default=False)),
                ('shifts', models.ManyToManyField(to='finance.Shift')),
            ],
        ),
        migrations.CreateModel(
            name='OneTimeFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('estimate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.estimate')),
            ],
        ),
        migrations.AddField(
            model_name='estimate',
            name='fees',
            field=models.ManyToManyField(blank=True, to='finance.Fee'),
        ),
    ]
