# Generated by Django 5.1.2 on 2024-10-19 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_alter_orderdealing_total_price_difference'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealingitem',
            name='is_seen_by_admin',
            field=models.BooleanField(default=False),
        ),
    ]
