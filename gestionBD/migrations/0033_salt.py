# Generated by Django 2.2.6 on 2020-06-20 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionBD', '0032_auto_20200620_2112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuarioUsuario', models.CharField(max_length=20, unique=True, verbose_name='Usuario')),
                ('salt', models.CharField(max_length=32, verbose_name='Salt')),
            ],
        ),
    ]
