# Generated by Django 5.1.2 on 2024-10-20 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0005_alter_packaging_bag_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyTotal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(verbose_name='الشهر')),
                ('year', models.IntegerField(verbose_name='السنة')),
                ('total_income', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='إجمالي الدخل')),
                ('total_costs', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='إجمالي التكلفة')),
                ('total_packaging', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='إجمالي التغليف')),
                ('goods_price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='سعر البضاعة')),
                ('total_profit', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='إجمال الربح')),
            ],
            options={
                'verbose_name': 'المجموع الشهري',
                'verbose_name_plural': 'المجموع الشهري',
            },
        ),
        migrations.AlterField(
            model_name='packaging',
            name='total',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10, verbose_name='الإجمالي'),
        ),
        migrations.AlterField(
            model_name='partners',
            name='name',
            field=models.CharField(max_length=250, verbose_name='الاسم'),
        ),
        migrations.AlterField(
            model_name='partners',
            name='share_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='النسبة'),
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='الاسم')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='التكلفة')),
                ('description', models.TextField(blank=True, null=True, verbose_name='الوصف')),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='costs', to='reportes.monthlytotal', verbose_name='شهر')),
            ],
            options={
                'verbose_name': 'تكلفة',
                'verbose_name_plural': 'التكاليف',
            },
        ),
        migrations.CreateModel(
            name='PackForMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_order_packing_cost', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='تكلفة تغليف الطلب الواحد')),
                ('for_month', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reportes.monthlytotal', verbose_name='مرتبط ب')),
            ],
        ),
    ]
