# Generated by Django 4.1.5 on 2023-04-27 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqrsdf', '0003_pqrsdffile_pqrsdf_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pqrsdf',
            old_name='file',
            new_name='file_id',
        ),
    ]
