# Generated by Django 4.2.16 on 2025-02-15 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_rename_quantity_product_stock_remove_product_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
