# Generated by Django 4.2 on 2024-08-27 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_devices_property_delete_user_devices_property'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Devices',
            new_name='Device',
        ),
    ]
