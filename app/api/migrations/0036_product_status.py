# Generated by Django 4.2.16 on 2025-02-15 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_product_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('pending', 'Pending')], default='pending', max_length=50),
        ),
    ]
