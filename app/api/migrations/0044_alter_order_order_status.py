# Generated by Django 4.2.16 on 2025-02-16 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_stock_min_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processsing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]),
        ),
    ]
