# Generated by Django 5.1.4 on 2025-02-09 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0025_rename_notes_booking_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='address',
        ),
    ]
