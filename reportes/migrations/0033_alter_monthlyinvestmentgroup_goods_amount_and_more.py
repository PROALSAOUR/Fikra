# Generated by Django 5.1.6 on 2025-04-27 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0032_alter_monthlyinvestmentgroup_monthly_percentage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyinvestmentgroup',
            name='goods_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='من البضاعة'),
        ),
        migrations.AlterField(
            model_name='monthlyinvestmentgroup',
            name='monthly_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='النسبة الشهرية'),
        ),
        migrations.AlterField(
            model_name='monthlyinvestmentgroup',
            name='profit_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='من الربح'),
        ),
        migrations.AlterField(
            model_name='monthlyinvestmentgroup',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name=' الإجمالي'),
        ),
        migrations.AlterField(
            model_name='storeprofit',
            name='goods_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='من البضاعة'),
        ),
        migrations.AlterField(
            model_name='storeprofit',
            name='monthly_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='النسبة الشهرية'),
        ),
        migrations.AlterField(
            model_name='storeprofit',
            name='profit_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='من الربح'),
        ),
        migrations.AlterField(
            model_name='storeprofit',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name=' الإجمالي'),
        ),
    ]
