# Generated by Django 2.2.6 on 2020-04-24 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0006_auto_20200422_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actividad',
            name='id',
        ),
        migrations.RemoveField(
            model_name='ofertaempleo',
            name='id',
        ),
        migrations.AlterField(
            model_name='actividad',
            name='enlaceAlbum',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='titulo',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='acuerdosempresas',
            name='texto',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datosdecontacto',
            name='facebook',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='datosdecontacto',
            name='instagram',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='datosdecontacto',
            name='twitter',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='datosdecontacto',
            name='ubicacion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='enlace',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='ofertaempleo',
            name='contacto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ofertaempleo',
            name='titulo',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ofertaempleotitulacion',
            name='ofertaEmpleo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionBD.OfertaEmpleo'),
        ),
        migrations.AlterField(
            model_name='usuarioactividad',
            name='actividad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionBD.Actividad'),
        ),
        migrations.AlterField(
            model_name='usuarioactividad',
            name='dniUsuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionBD.Usuario'),
        ),
    ]