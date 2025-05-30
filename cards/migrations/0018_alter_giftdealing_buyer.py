# Generated by Django 5.1.2 on 2024-10-17 09:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0017_giftdealing_buyer_giftdealing_message_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftdealing',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gift_dealing_buyer', to=settings.AUTH_USER_MODEL),
        ),
    ]
