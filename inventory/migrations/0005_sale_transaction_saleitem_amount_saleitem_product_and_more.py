# Generated by Django 4.1.7 on 2023-05-06 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_remove_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='transaction',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='inventory.transaction'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saleitem',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inventory.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saleitem',
            name='sale_amount',
            field=models.IntegerField(default=0),
        ),
    ]
