# Generated by Django 2.2.6 on 2020-08-04 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0036_auto_20200804_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='hora',
            field=models.TimeField(blank=True, null=True, verbose_name='Hora de la actividad'),
        ),
    ]