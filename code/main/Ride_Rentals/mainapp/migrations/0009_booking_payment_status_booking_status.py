# Generated by Django 5.1.3 on 2025-01-06 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('booked', 'Booked'), ('rented', 'Rented'), ('completed', 'Completed')], default='booked', max_length=10),
        ),
    ]
