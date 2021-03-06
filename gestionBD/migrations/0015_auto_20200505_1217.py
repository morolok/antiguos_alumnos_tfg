# Generated by Django 2.2.6 on 2020-05-05 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0014_auto_20200505_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='fechaSolicitudesFin',
            field=models.DateField(null=True, verbose_name='Fecha de fin de las solicitudes'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='fechaSolicitudesInicio',
            field=models.DateField(null=True, verbose_name='Fecha de nicio de las solicitudes'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='numeroPlazas',
            field=models.IntegerField(null=True, verbose_name='Número de plazas'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='fecha',
            field=models.DateField(verbose_name='Fecha de la actividad'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='hora',
            field=models.TimeField(blank=True, null=True, verbose_name='Hora de la actividad'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Imagen'),
        ),
    ]
