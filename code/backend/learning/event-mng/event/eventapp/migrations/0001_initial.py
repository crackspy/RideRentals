# Generated by Django 5.1.3 on 2024-12-16 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='pic')),
                ('name', models.CharField(max_length=50)),
                ('dec', models.CharField(max_length=50)),
            ],
        ),
    ]
