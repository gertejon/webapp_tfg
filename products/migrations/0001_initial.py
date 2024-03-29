# Generated by Django 4.2 on 2023-05-08 17:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(default='', max_length=100)),
                ('product_type', models.CharField(default='', max_length=100)),
                ('manufacturer', models.CharField(default='', max_length=100)),
                ('quality', models.CharField(default='', max_length=100)),
                ('price', models.FloatField()),
                ('specs', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=list, size=None)),
                ('accessories_id', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None)),
                ('instrument', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to='product_images/')),
            ],
        ),
    ]
