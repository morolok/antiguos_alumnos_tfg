# Generated by Django 2.2.6 on 2020-04-28 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0008_auto_20200428_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='juntaRectora',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionBD.JuntaRectora'),
        ),
    ]
