# Generated by Django 5.1.5 on 2025-02-20 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0029_remove_order_message_remove_order_with_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='discount_share',
            field=models.IntegerField(default=0, verbose_name='نصيب الخصم'),
        ),
    ]
