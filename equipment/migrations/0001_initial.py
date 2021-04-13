# Generated by Django 3.2 on 2021-04-13 02:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_addon', models.BooleanField(default=False)),
                ('department', models.CharField(choices=[('L', 'Lighting'), ('S', 'Sound'), ('M', 'Manager'), ('O', 'Other')], max_length=1)),
                ('base_price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('price_per_hour', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BrokenEquipmentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_filed', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField()),
                ('investigation', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('U', 'Unread'), ('A', 'Acknowledged'), ('W', 'WIP'), ('B', 'Blocked'), ('C', 'Closed')], max_length=1, null=True)),
                ('broken_system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.system')),
                ('reported_broken_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
