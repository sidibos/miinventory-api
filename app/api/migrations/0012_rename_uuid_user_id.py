# Generated by Django 4.2.16 on 2025-02-09 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_user_id_user_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='uuid',
            new_name='id',
        ),
    ]
