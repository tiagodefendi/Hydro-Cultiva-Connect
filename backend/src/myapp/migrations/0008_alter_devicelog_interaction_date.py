# Generated by Django 5.1 on 2024-09-07 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_device_status_devicelog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicelog',
            name='interaction_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
