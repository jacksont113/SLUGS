# Generated by Django 3.2.2 on 2021-05-11 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0013_merge_20210511_1218'),
        ('employee', '0003_alter_officehours_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officehours',
            name='position',
            field=models.ForeignKey(default='Manager', on_delete=django.db.models.deletion.PROTECT, to='auth.group', to_field='name'),
        ),
    ]
