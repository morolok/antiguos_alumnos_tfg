# Generated by Django 2.2.6 on 2021-06-16 18:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0055_auto_20210616_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumfotos',
            name='enlace',
            field=models.URLField(validators=[django.core.validators.URLValidator()], verbose_name='Enlace'),
        ),
    ]
