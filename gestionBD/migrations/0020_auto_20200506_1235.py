# Generated by Django 2.2.6 on 2020-05-06 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0019_auto_20200505_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='fichero',
            field=models.FileField(blank=True, upload_to='files', verbose_name='Fichero'),
        ),
    ]
