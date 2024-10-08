# Generated by Django 5.0.7 on 2024-08-03 03:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_products_category_id_products_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='product_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.products'),
        ),
        migrations.AddField(
            model_name='orders',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payments',
            name='status',
            field=models.CharField(choices=[('DONE', 'Done'), ('CANCEL', 'Cancel'), ('WAITING', 'Waiting')], default='WAITING', max_length=10),
        ),
        migrations.DeleteModel(
            name='OrderItems',
        ),
    ]
