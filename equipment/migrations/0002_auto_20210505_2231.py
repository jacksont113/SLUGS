# Generated by Django 3.2 on 2021-05-06 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("equipment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="system",
            name="description",
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name="systemaddon",
            name="description",
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
