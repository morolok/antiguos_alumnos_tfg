# Generated by Django 2.2.6 on 2020-04-28 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0007_auto_20200424_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('tipo', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo',
            field=models.CharField(max_length=50),
        ),
    ]
