# Generated by Django 4.1.4 on 2023-01-04 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pqrsdf', '0005_alter_pqrsdf_date_pqrsdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='pqrsdf',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Activo'),
        ),
    ]
