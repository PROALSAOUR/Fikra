# Generated by Django 5.1.2 on 2024-10-17 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0022_remove_giftdealing_receive'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftdealing',
            name='receive',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dealing', to='cards.receivegift'),
        ),
    ]
