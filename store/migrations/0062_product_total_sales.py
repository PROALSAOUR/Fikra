# Generated by Django 5.1.2 on 2024-10-18 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0061_remove_product_sales_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='total_sales',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
