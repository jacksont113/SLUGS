# Generated by Django 3.2 on 2021-04-12 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("utils", "0002_alter_notification_message"),
    ]

    operations = [
        migrations.CreateModel(
            name="signupStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_open", models.BooleanField()),
            ],
        ),
    ]
