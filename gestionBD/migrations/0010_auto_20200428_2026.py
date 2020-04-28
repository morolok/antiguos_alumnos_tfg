# Generated by Django 2.2.6 on 2020-04-28 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0009_auto_20200428_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='tipoActividad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionBD.TipoActividad'),
        ),
        migrations.AlterField(
            model_name='ofertaempleotitulacion',
            name='titulacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionBD.Titulacion'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionBD.TipoUsuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='titulacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionBD.Titulacion'),
        ),
    ]
