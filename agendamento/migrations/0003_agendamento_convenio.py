# Generated by Django 5.0.2 on 2024-06-13 23:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamento', '0002_agendamento_data_hora_sistema_and_more'),
        ('convenios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='convenio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='convenios.convenio'),
        ),
    ]
