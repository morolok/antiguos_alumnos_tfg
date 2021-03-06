# Generated by Django 2.2.6 on 2020-05-05 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0013_auto_20200503_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='descripcion',
            field=models.TextField(verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='hora',
            field=models.TimeField(blank=True, null=True, verbose_name='Hora'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='textoReseña',
            field=models.TextField(blank=True, null=True, verbose_name='Texto de reseña'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='titulo',
            field=models.CharField(max_length=1024, primary_key=True, serialize=False, verbose_name='Título'),
        ),
    ]
