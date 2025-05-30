# Generated by Django 5.1.5 on 2025-02-26 16:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0042_alter_dealingitem_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='المدينة'),
        ),
        migrations.AddField(
            model_name='order',
            name='neighborhood',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=' الحي'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='المستخدم'),
        ),
    ]
