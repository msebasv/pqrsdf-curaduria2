# Generated by Django 4.1.4 on 2023-01-24 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqrsdf', '0016_pqrsdfstate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pqrsdfstate',
            name='id_pqrsdf',
        ),
        migrations.RemoveField(
            model_name='pqrsdfstate',
            name='id_user',
        ),
        migrations.DeleteModel(
            name='Pqrsdf',
        ),
        migrations.DeleteModel(
            name='PqrsdfState',
        ),
    ]