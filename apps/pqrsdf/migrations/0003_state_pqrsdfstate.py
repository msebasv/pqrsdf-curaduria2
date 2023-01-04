# Generated by Django 4.1.4 on 2023-01-04 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pqrsdf', '0002_alter_pqrsdf_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=30, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'State',
                'verbose_name_plural': 'States',
            },
        ),
        migrations.CreateModel(
            name='PqrsdfState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_input', models.DateField(blank=True, null=True, verbose_name='Fecha Entrada')),
                ('date_out', models.DateField(blank=True, null=True, verbose_name='Fecha Salida')),
                ('user_change_input', models.CharField(blank=True, max_length=191, null=True, verbose_name='Usuario entrada')),
                ('user_change_output', models.CharField(blank=True, max_length=10, null=True, verbose_name='Usuario Salida')),
                ('id_pqrsdf', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pqrsdf.pqrsdf')),
                ('id_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pqrsdf.state')),
            ],
            options={
                'verbose_name': 'PqrsdfState',
                'verbose_name_plural': 'PqrsdfStates',
            },
        ),
    ]
