# Generated by Django 5.1.2 on 2024-10-20 16:17

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0025_remove_giftdealing_buyer'),
        ('store', '0063_alter_adsproducts_ads_name_alter_adsproducts_product_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='copon',
            name='code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length=12, max_length=20, prefix='', unique=True, verbose_name='الكود'),
        ),
        migrations.AlterField(
            model_name='copon',
            name='expiration_days',
            field=models.IntegerField(default=365, verbose_name='يفسد بعد'),
        ),
        migrations.AlterField(
            model_name='copon',
            name='img',
            field=models.ImageField(upload_to='store/Cards/Copons', verbose_name='الصورة'),
        ),
        migrations.AlterField(
            model_name='copon',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='مفعل؟'),
        ),
        migrations.AlterField(
            model_name='copon',
            name='min_bill_price',
            field=models.PositiveIntegerField(verbose_name='اقل قيمة للإستعمال'),
        ),
        migrations.AlterField(
            model_name='copon',
            name='name',
            field=models.CharField(max_length=30, verbose_name='الاسم'),
        ),
        migrations.AlterField(
            model_name='copon',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='السعر'),
        ),
        migrations.AlterField(
            model_name='copon',
            name='sales_count',
            field=models.PositiveIntegerField(default=0, verbose_name='عدد المبيعات'),
        ),
        migrations.AlterField(
            model_name='copon',
            name='tags',
            field=models.ManyToManyField(blank=True, to='store.tag', verbose_name='الهاشتاج'),
        ),
        migrations.AlterField(
            model_name='copon',
            name='value',
            field=models.PositiveIntegerField(verbose_name='القيمة'),
        ),
        migrations.AlterField(
            model_name='coponusage',
            name='copon_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copon_usage', to='cards.copon', verbose_name='الكود'),
        ),
        migrations.AlterField(
            model_name='coponusage',
            name='expire',
            field=models.DateField(blank=True, null=True, verbose_name='تاريخ انتهاء الصلاحية'),
        ),
        migrations.AlterField(
            model_name='coponusage',
            name='has_used',
            field=models.BooleanField(default=False, verbose_name='حالة الاستعمال'),
        ),
        migrations.AlterField(
            model_name='coponusage',
            name='purchase_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الشراء'),
        ),
        migrations.AlterField(
            model_name='coponusage',
            name='sell_price',
            field=models.IntegerField(default=0, verbose_name='السعر'),
        ),
        migrations.AlterField(
            model_name='coponusage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='المشتري'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length=12, max_length=20, prefix='', unique=True, verbose_name='الكود'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='img',
            field=models.ImageField(upload_to='store/Cards/Gifts', verbose_name='الصورة'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='مفعل؟'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='name',
            field=models.CharField(max_length=30, verbose_name='الاسم'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='price',
            field=models.PositiveIntegerField(verbose_name='السعر'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='sales_count',
            field=models.PositiveIntegerField(default=0, verbose_name='عدد المبيعات'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='tags',
            field=models.ManyToManyField(blank=True, to='store.tag', verbose_name='الهاشتاج'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='value',
            field=models.PositiveIntegerField(verbose_name='القيمة'),
        ),
        migrations.AlterField(
            model_name='giftdealing',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='تاريخ الإنشاء'),
        ),
        migrations.AlterField(
            model_name='giftdealing',
            name='is_dealt',
            field=models.BooleanField(default=False, verbose_name='معالجة؟'),
        ),
        migrations.AlterField(
            model_name='giftdealing',
            name='message',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='الرسالة'),
        ),
        migrations.AlterField(
            model_name='giftdealing',
            name='receive',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dealing', to='cards.receivegift', verbose_name='كود الاستلام'),
        ),
        migrations.AlterField(
            model_name='giftdealing',
            name='receiver_name',
            field=models.CharField(max_length=50, verbose_name='اسم المستلم'),
        ),
        migrations.AlterField(
            model_name='giftdealing',
            name='receiver_phone',
            field=models.CharField(max_length=20, verbose_name='رقم المستلم'),
        ),
        migrations.AlterField(
            model_name='giftdealing',
            name='sell_price',
            field=models.PositiveIntegerField(default=0, verbose_name='السعر'),
        ),
        migrations.AlterField(
            model_name='giftdealing',
            name='sell_value',
            field=models.PositiveIntegerField(default=0, verbose_name='القيمة'),
        ),
        migrations.AlterField(
            model_name='giftdealing',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='المرسل'),
        ),
        migrations.AlterField(
            model_name='giftdealing',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='تاريخ التعديل'),
        ),
        migrations.AlterField(
            model_name='giftitem',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gift_items_buyer', to=settings.AUTH_USER_MODEL, verbose_name='المشتري'),
        ),
        migrations.AlterField(
            model_name='giftitem',
            name='gift',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gift_items', to='cards.gift', verbose_name='الهدية'),
        ),
        migrations.AlterField(
            model_name='giftitem',
            name='has_used',
            field=models.BooleanField(default=False, verbose_name='مستعمل؟'),
        ),
        migrations.AlterField(
            model_name='giftitem',
            name='is_seen',
            field=models.BooleanField(default=False, verbose_name='مشاهدة؟'),
        ),
        migrations.AlterField(
            model_name='giftitem',
            name='purchase_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الشراء'),
        ),
        migrations.AlterField(
            model_name='giftitem',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gift_items_recipient', to=settings.AUTH_USER_MODEL, verbose_name='المستلم'),
        ),
        migrations.AlterField(
            model_name='giftitem',
            name='sell_price',
            field=models.PositiveIntegerField(default=0, verbose_name='سعر الشراء'),
        ),
        migrations.AlterField(
            model_name='giftitem',
            name='sell_value',
            field=models.PositiveIntegerField(default=0, verbose_name='القيمة'),
        ),
        migrations.AlterField(
            model_name='giftrecipient',
            name='gift_item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='gift_recipients', to='cards.giftitem', verbose_name='عنصر الهدية'),
        ),
        migrations.AlterField(
            model_name='giftrecipient',
            name='message',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='الرسالة'),
        ),
        migrations.AlterField(
            model_name='giftrecipient',
            name='recipient_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='اسم المستلم'),
        ),
        migrations.AlterField(
            model_name='giftrecipient',
            name='recipient_phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='رقم الهاتف'),
        ),
        migrations.AlterField(
            model_name='receivegift',
            name='code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length=12, max_length=20, prefix='', unique=True, verbose_name='الكود'),
        ),
        migrations.AlterField(
            model_name='receivegift',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='تاريخ الإنشاء'),
        ),
        migrations.AlterField(
            model_name='receivegift',
            name='gift',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receive_gift', to='cards.gift', verbose_name='الهدية'),
        ),
        migrations.AlterField(
            model_name='receivegift',
            name='is_used',
            field=models.BooleanField(default=False, verbose_name='مستعمل؟'),
        ),
        migrations.AlterField(
            model_name='receivegift',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='تاريخ التعديل'),
        ),
        migrations.AlterField(
            model_name='receivegift',
            name='value',
            field=models.PositiveIntegerField(verbose_name='القيمة'),
        ),
    ]
