# Generated by Django 5.1.2 on 2024-10-19 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'عدد الطلبات',
            },
        ),
    ]
