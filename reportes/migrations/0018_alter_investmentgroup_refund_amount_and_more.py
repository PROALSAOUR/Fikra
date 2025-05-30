# Generated by Django 5.1.2 on 2024-10-21 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0017_investmentgroup_ready_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentgroup',
            name='refund_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='المبلغ المسترد'),
        ),
        migrations.AlterField(
            model_name='investmentgroup',
            name='remaining_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='المبلغ المتبقي'),
        ),
        migrations.AlterField(
            model_name='investmentgroup',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='الحصة'),
        ),
    ]
