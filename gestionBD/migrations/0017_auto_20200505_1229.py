# Generated by Django 2.2.6 on 2020-05-05 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0016_actividad_fichero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='fechaSolicitudesInicio',
            field=models.DateField(null=True, verbose_name='Fecha de inicio de las solicitudes'),
        ),
    ]
