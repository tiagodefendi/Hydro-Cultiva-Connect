# Generated by Django 5.1 on 2024-09-07 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_device_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='status',
            field=models.CharField(default='off', max_length=50),
        ),
    ]