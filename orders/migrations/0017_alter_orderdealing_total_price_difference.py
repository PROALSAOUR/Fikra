# Generated by Django 5.1.2 on 2024-10-19 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_remove_orderdealing_status_remove_orderdealing_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdealing',
            name='total_price_difference',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
