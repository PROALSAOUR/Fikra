from django.db import models
from django.utils.timezone import now  
from shortuuid.django_fields import ShortUUIDField
from store.models import Tag
from accounts.models import User
import string
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from datetime import timedelta

# ============================= Cards ====================================

class Copon(models.Model):
    code = ShortUUIDField(unique=True, length=12, max_length=20, alphabet= string.ascii_uppercase + string.digits , verbose_name='الكود')
    name = models.CharField(max_length=30 , verbose_name='الاسم')
    img = models.ImageField(upload_to='store/Cards/Copons', verbose_name='الصورة')
    value = models.PositiveIntegerField( verbose_name='القيمة')
    min_bill_price = models.PositiveIntegerField(verbose_name='اقل قيمة للإستعمال')
    price = models.PositiveIntegerField(default=0, verbose_name='السعر')
    is_active = models.BooleanField(default=True, verbose_name='مفعل؟')
    expiration_days = models.IntegerField(default=365, verbose_name='يفسد بعد') # عدد الايام التي يفسد بعدها الكوبون
    sales_count = models.PositiveIntegerField(default=0, verbose_name='عدد المبيعات')  # عدد مرات بيع الكوبون
    tags = models.ManyToManyField(Tag,  blank=True, verbose_name='الهاشتاج')

    def __str__(self):
        return self.name
     
    def copon_image(self):
        # دالة مسؤولة عن عرض صورة المنتج المصغرة في لوحة الادارة
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.img.url) )
      
    def clean(self):
        # تحقق إذا كانت القيمة أكبر من 100
        if self.value > 100:
            raise ValidationError("القيمة للكوبون يجب أن تكون اصغر من أو تساوي 100.")
        super(Copon, self).clean()

    def save(self, *args, **kwargs):
        # تنفيذ clean للتأكد من التحقق قبل الحفظ
        self.clean()
        super(Copon, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'كوبون خصم'
        verbose_name_plural = 'كوبونات الخصم'
    
class CoponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name='المشتري')  # المستخدم الذي اشترى الرمز
    copon_code = models.ForeignKey(Copon, on_delete=models.CASCADE, related_name='copon_usage' , verbose_name='الكود')  # رمز الخصم
    sell_price = models.IntegerField(default=0, verbose_name='السعر') # سعر الكوبون عندما اشتراه المستخدم
    has_used = models.BooleanField(default=False, verbose_name='حالة الاستعمال')  # لتتبع إذا استخدم المستخدم الرمز
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الشراء')  # وقت شراء الرمز
    expire = models.DateField(null=True, blank=True, verbose_name='تاريخ انتهاء الصلاحية')
    
    def is_expire(self):
        if self.expire:
            if self.expire >= now().date():
                return False
            else:
                return True
    
    def use_copon(self):
        self.has_used = True
        self.expire = None
        self.save()
    
    def buy_copon(self):
        self.has_used = False # الكوبون غير مستخدم بعد الشراء
        self.expire = now().date() + timedelta(days=self.copon_code.expiration_days) # صلاحية جديدة عد اتمام الشراء
        self.sell_price = self.copon_code.price # سعر شراء الكوبون
        self.save()
    
    def __str__(self):
        return f"{self.user.first_name} - {self.copon_code.code}"
        
    class Meta:
        verbose_name = 'سجلات شراء الكوبونات'
        verbose_name_plural = 'سجلات شراء الكوبونات'
    
class Gift(models.Model):
    code = ShortUUIDField(unique=True, length=12, max_length=20, alphabet= string.ascii_uppercase + string.digits , verbose_name='الكود')
    name = models.CharField(max_length=30, verbose_name='الاسم')
    img = models.ImageField(upload_to='store/Cards/Gifts', verbose_name='الصورة')
    value = models.PositiveIntegerField( verbose_name='القيمة')  # قيمة الهدية
    price = models.PositiveIntegerField(verbose_name='السعر')  # سعر الشراء بالنقاط أو المال
    is_active = models.BooleanField(default=True , verbose_name='مفعل؟')  # حالة الهدية (نشطة أو غير نشطة)
    sales_count = models.PositiveIntegerField(default=0, verbose_name='عدد المبيعات')  # عدد مرات بيع الهدية
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='الهاشتاج')
    
    def __str__(self):
        return self.name

    def gift_image(self):
        return mark_safe(f"<img src='{self.img.url}' width='50' height='50' />")

    class Meta:
        verbose_name = 'كرت هدية'
        verbose_name_plural = 'كروت هدايا'   

class GiftItem(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE, related_name='gift_items', verbose_name='الهدية')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gift_items_buyer', verbose_name='المشتري')  # المستخدم الذي اشترى الهدية
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gift_items_recipient', null=True, verbose_name='المستلم')  # المستخدم الذي له الهدية
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الشراء')  # وقت الشراء
    sell_price = models.PositiveIntegerField(default=0, verbose_name='سعر الشراء') # سعر  عندما اشتراه المستخدم
    sell_value = models.PositiveIntegerField(default=0, verbose_name='القيمة') # القيمة عند الشراء
    has_used = models.BooleanField(default=False, verbose_name='مستعمل؟') # هل تم استخدام الهدية أم لا
    is_seen = models.BooleanField(default=False, verbose_name='مشاهدة؟') # هل شاهد المستخدم الهدية؟

    def save(self, *args, **kwargs):
        if self.buyer == self.recipient:
            self.is_seen = True
        super(GiftItem, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.buyer} - {self.gift.name}"

    class Meta:
        verbose_name = 'سجل شراء هدية'
        verbose_name_plural = ' سجلات شراء الهدايا'
        
    # دالة للتحقق مما إذا كان هناك GiftRecipient مرتبط
    def has_recipient(self):
        return self.recipient is not None

class GiftRecipient(models.Model):
    gift_item = models.OneToOneField(GiftItem, on_delete=models.CASCADE, related_name='gift_recipients', verbose_name='عنصر الهدية')
    recipient_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='اسم المستلم')  # اسم المستلم
    recipient_phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='رقم الهاتف')  # هاتف المستلم
    message = models.TextField(blank=True, null=True, max_length=300, verbose_name='الرسالة')  # رسالة شخصية
    
    def __str__(self):
        return f"هدية{self.gift_item.pk} إلى: {self.recipient_name or 'نفسه'}"
    
    class Meta:
        verbose_name = 'مستلم هدية'
        verbose_name_plural = 'مستلمو الهدايا'

class ReceiveGift(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE, related_name='receive_gift', verbose_name='الهدية')
    code = ShortUUIDField(unique=True, length=12, max_length=20, alphabet= string.ascii_uppercase + string.digits, verbose_name='الكود')  # كود فريد لهذه الهدية المشتراة
    is_used = models.BooleanField(default=False, verbose_name='مستعمل؟')
    value = models.PositiveIntegerField(verbose_name='القيمة')
    created_at = models.DateField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateField(auto_now=True, verbose_name='تاريخ التعديل')
        
    def __str__(self):
        return f'{self.gift.name}, {self.value}'
        
    class Meta:
        verbose_name = 'كود استلام هدية'
        verbose_name_plural = 'اكواد استلام هدايا'

class GiftDealing(models.Model):
    '''
    في حال ارسل احدهم هدية الى شخص ولم يكن مستعملا للبرنامج
    يتم التواصل معه بواسطة خدمة العملاء من هنا
    '''
    
    sell_price = models.PositiveIntegerField(default=0, verbose_name='السعر') # سعر  عندما اشتراه المستخدم
    sell_value = models.PositiveIntegerField(default=0, verbose_name='القيمة') # القيمة عند الشراء
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='المرسل')
    receiver_name = models.CharField(max_length=50, verbose_name='اسم المستلم')
    receiver_phone = models.CharField(max_length=20, verbose_name='رقم المستلم')
    message = models.TextField(blank=True, null=True, max_length=300, verbose_name='الرسالة')  # رسالة شخصية
    is_dealt = models.BooleanField(default=False, verbose_name='معالجة؟')
    receive = models.ForeignKey(ReceiveGift, on_delete=models.CASCADE, related_name='dealing', null=True, verbose_name='كود الاستلام')
    created_at = models.DateField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateField(auto_now=True, verbose_name='تاريخ التعديل')
    
        
    def __str__(self):
        return f"هدية إلى: {self.receiver_name} من: {self.sender}"
    
    class Meta:
        verbose_name = 'ايصال هدية'
        verbose_name_plural = 'ايصال هدايا'
      
# ================== Functions ================================================

