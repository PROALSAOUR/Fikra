# Generated by Django 5.1.6 on 2025-03-16 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0010_alter_settings_expected_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='social',
            name='instagram',
        ),
        migrations.AddField(
            model_name='social',
            name='tiktok',
            field=models.URLField(blank=True, verbose_name='فيكتوك'),
        ),
    ]
