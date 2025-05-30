# Generated by Django 5.1.6 on 2025-04-27 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0031_monthlytotal_contributing_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyinvestmentgroup',
            name='monthly_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='النسبة الشهرية'),
        ),
        migrations.AlterField(
            model_name='storeprofit',
            name='monthly_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='النسبة الشهرية'),
        ),
    ]
