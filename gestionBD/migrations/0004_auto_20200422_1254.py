# Generated by Django 2.2.6 on 2020-04-22 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0003_auto_20200417_2055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acuerdosempresas',
            old_name='text0',
            new_name='texto',
        ),
    ]
