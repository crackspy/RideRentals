# Generated by Django 5.1.5 on 2025-02-05 02:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0016_booking_profile_profile_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.profile'),
        ),
    ]
