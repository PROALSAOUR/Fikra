# Generated by Django 5.1.1 on 2024-10-07 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_giftdealing_sell_price_giftdealing_sell_value_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftrecipient',
            name='gift_for',
        ),
    ]
