# Generated by Django 5.1.6 on 2025-02-17 11:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_point_table_delete_datapoint'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalculationResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=100)),
                ('iterations_count', models.IntegerField()),
                ('parameter_a', models.FloatField()),
                ('parameter_b', models.FloatField()),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.table')),
            ],
        ),
    ]
