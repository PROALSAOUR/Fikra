from django.db import models
from django.utils.timezone import now  
from shortuuid.django_fields import ShortUUIDField
from store.models import Tag
from accounts.models import User
import string
from django.utils.html import mark_safe
from datetime import timedelta

# ============================= Cards ====================================

class Copon(models.Model):
    code = ShortUUIDField(unique=True, length=12, max_length=20, alphabet= string.ascii_uppercase + string.digits , verbose_name='الكود')
    name = models.CharField(max_length=30 , verbose_name='الاسم')
    img = models.ImageField(upload_to='store/Cards/Copons', verbose_name='الصورة')
    value = models.PositiveIntegerField( verbose_name='القيمة')
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
    
    class Meta:
        verbose_name = 'كوبون خصم'
        verbose_name_plural = 'كوبونات الخصم'
    
class CoponItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name='المشتري')  # المستخدم الذي اشترى الرمز
    copon_code = models.ForeignKey(Copon, on_delete=models.CASCADE, related_name='copon_usage' , verbose_name='الكوبون')  
    sell_price = models.IntegerField(default=0, verbose_name='سعر البيع بالنقاط') # سعر الكوبون عندما اشتراه المستخدم
    has_used = models.BooleanField(default=False, verbose_name='حالة الاستعمال')  # لتتبع إذا استخدم المستخدم الرمز
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الشراء')  # وقت شراء الرمز
    expire = models.DateField(null=True, blank=True, verbose_name='تاريخ انتهاء الصلاحية')
    receive_from_code = models.BooleanField(default=False, verbose_name='استلم من كود؟')
    def is_expire(self):
        if self.expire:
            if self.expire >= now().date():
                return False
            else:
                return True
        else:
            return False
    
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

class ReceiveCopon(models.Model):
    copon = models.ForeignKey(Copon, on_delete=models.CASCADE, related_name='receive_copon', verbose_name='الكوبون')
    code = ShortUUIDField(unique=True, length=12, max_length=20, alphabet= string.ascii_uppercase + string.digits, verbose_name='الكود')  # كود فريد لهذا الكوبون المشتراة
    is_used = models.BooleanField(default=False, verbose_name='مستعمل؟')
    used_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user' , verbose_name='استعمل بواسطة') # اذا كان مستخدما يتم انشاء علاقة مع المستخدم الذي اساخدمه
    created_at = models.DateField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateField(auto_now=True, verbose_name='تاريخ التعديل')
        
    def __str__(self):
        return f'كود استلام ل{self.copon.name}'
        
    class Meta:
        verbose_name = 'كود استلام كوبون'
        verbose_name_plural = 'اكواد استلام كوبونات'
  
# ================== Functions ================================================