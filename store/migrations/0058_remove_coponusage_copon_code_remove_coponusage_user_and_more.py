# Generated by Django 5.1.1 on 2024-10-04 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0057_alter_giftdealing_receiver_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coponusage',
            name='copon_code',
        ),
        migrations.RemoveField(
            model_name='coponusage',
            name='user',
        ),
        migrations.RemoveField(
            model_name='gift',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='giftitem',
            name='gift',
        ),
        migrations.RemoveField(
            model_name='giftdealing',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='giftitem',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='giftitem',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='giftrecipient',
            name='gift_item',
        ),
        migrations.DeleteModel(
            name='Copon',
        ),
        migrations.DeleteModel(
            name='CoponUsage',
        ),
        migrations.DeleteModel(
            name='Gift',
        ),
        migrations.DeleteModel(
            name='GiftDealing',
        ),
        migrations.DeleteModel(
            name='GiftItem',
        ),
        migrations.DeleteModel(
            name='GiftRecipient',
        ),
    ]
