# Generated by Django 3.0.6 on 2020-06-16 05:54

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewEmployeesAllowed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_open', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Allow new Employees?',
                'verbose_name_plural': 'Allow new Employees?',
            },
        ),
        migrations.CreateModel(
            name='Wage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=11.8, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('message', models.TextField()),
                ('message_type', models.CharField(choices=[('normal', 'Normal'), ('uk-alert-success', 'Success'), ('uk-alert-warning', 'Warning'), ('uk-alert-danger', 'Danger/Error')], default='normal', max_length=16)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('groups_to_send_to', models.ManyToManyField(blank=True, help_text='Send the notification to the following groups.', to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('bnum', models.IntegerField(null=True, verbose_name='B Number')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
                ('active', models.BooleanField(default=False, verbose_name='Current Employee')),
                ('staff', models.BooleanField(default=False, verbose_name='Manager')),
                ('admin', models.BooleanField(default=False, verbose_name='System Admin')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
