# Generated by Django 4.2 on 2023-05-12 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_alter_location_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
