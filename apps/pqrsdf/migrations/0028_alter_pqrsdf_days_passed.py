# Generated by Django 4.1.5 on 2023-04-13 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqrsdf', '0027_pqrsdf_days_passed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pqrsdf',
            name='days_passed',
            field=models.IntegerField(default=0, verbose_name='Días transcurridos'),
        ),
    ]
