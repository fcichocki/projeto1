# Generated by Django 5.0.2 on 2024-03-31 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anamnese',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anamnese', models.CharField(max_length=200)),
            ],
        ),
    ]
