# Generated by Django 5.1.6 on 2025-03-21 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0011_remove_social_instagram_social_tiktok'),
    ]

    operations = [
        migrations.AlterField(
            model_name='social',
            name='tiktok',
            field=models.URLField(blank=True, verbose_name='تيكتوك'),
        ),
    ]
