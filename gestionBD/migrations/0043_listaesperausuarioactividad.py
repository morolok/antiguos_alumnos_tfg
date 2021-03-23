# Generated by Django 2.2.6 on 2021-03-23 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0042_auto_20210304_1938'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaEsperaUsuarioActividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionBD.Actividad', verbose_name='Actividad')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionBD.Usuario', verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Lista de espera usuario actividad',
                'verbose_name_plural': 'Lista de usuarios actividades',
            },
        ),
    ]
