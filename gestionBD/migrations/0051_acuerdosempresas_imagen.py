# Generated by Django 2.2.6 on 2021-06-09 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0050_actividad_estadoactividad'),
    ]

    operations = [
        migrations.AddField(
            model_name='acuerdosempresas',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Imagen'),
        ),
    ]
