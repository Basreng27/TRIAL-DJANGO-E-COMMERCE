# Generated by Django 5.0.7 on 2024-08-05 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_orders_price_orders_product_id_orders_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='order_id',
        ),
        migrations.DeleteModel(
            name='Orders',
        ),
        migrations.DeleteModel(
            name='Payments',
        ),
    ]
