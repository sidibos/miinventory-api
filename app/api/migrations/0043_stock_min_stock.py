# Generated by Django 4.2.16 on 2025-02-16 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_alter_order_order_type_alter_order_pay'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='min_stock',
            field=models.IntegerField(default=0),
        ),
    ]
