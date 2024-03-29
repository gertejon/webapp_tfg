# Generated by Django 4.2 on 2023-05-11 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0001_initial'),
        ('product_types', '0001_initial'),
        ('products', '0002_alter_product_category_alter_product_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='accessories_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='instrument',
        ),
        migrations.RemoveField(
            model_name='product',
            name='manufacturer',
        ),
        migrations.AddField(
            model_name='product',
            name='accessories',
            field=models.ManyToManyField(to='products.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='brands.brand'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_accessory',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_types.product_type'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quality',
            field=models.CharField(choices=[('HIGH-END', 'High-end'), ('MID-RANGE', 'Mid-range'), ('BUDGET', 'Affordable')], default='Mid-range', max_length=10),
        ),
    ]
