# Generated by Django 2.2.12 on 2020-07-10 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='id_default',
            new_name='is_default',
        ),
    ]