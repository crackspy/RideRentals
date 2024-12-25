# Generated by Django 5.1.4 on 2024-12-25 08:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0002_car_info_slug_car_info_year"),
    ]

    operations = [
        migrations.AddField(
            model_name="car_info",
            name="price",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="car_info",
            name="mileage",
            field=models.FloatField(),
        ),
    ]
