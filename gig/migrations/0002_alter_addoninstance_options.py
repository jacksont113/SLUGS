# Generated by Django 3.2 on 2021-05-06 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gig", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="addoninstance",
            options={"verbose_name": "Addon", "verbose_name_plural": "Addons"},
        ),
    ]
