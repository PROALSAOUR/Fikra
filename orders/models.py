from django.db import models
from django.utils.html import mark_safe
from store.models import ProductVariation
from django.core.exceptions import ValidationError
from accounts.models import User
        
class Order(models.Model):
    
    ORDER_STATUS = [
        ('pending', 'جاري المعالجة'),
        ('checking', 'جاري التجهيز'),
        ('shipped', 'جاري الشحن'),
        ('delivered', 'تم التسليم'),
        ('canceled', 'تم الإلغاء'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders' , verbose_name='المستخدم')
    phone_number = models.CharField(max_length=20, verbose_name='رقم المستلم', blank=True)
    serial_number = models.IntegerField(unique=True, verbose_name='الرقم التسلسلي')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending' , verbose_name='الحالة')
    old_total = models.IntegerField(verbose_name='الإجمالي القديم')
    total_price = models.IntegerField(verbose_name='الإجمالي')
    total_points = models.PositiveIntegerField(null=True, verbose_name='المكافأة')
    copon_value = models.IntegerField(default=0, verbose_name='قيمة الكوبون')
    used_discount = models.IntegerField(default=0, verbose_name='الخصم المستعمل')
    free_delivery =  models.BooleanField(default=False, verbose_name='توصيل مجاني؟')
    delivery_price = models.IntegerField(default=0, verbose_name='سعر التوصيل')
    city = models.CharField(max_length=100, verbose_name='المدينة', blank=True, null=True)
    neighborhood = models.CharField(max_length=100, verbose_name=' الحي', blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الطلب')
    deliverey_date = models.DateTimeField(null=True, blank=True, verbose_name='تاريخ التسليم')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')
    note = models.TextField(null=True, blank=True, verbose_name='ملاحظة')
        
    def get_total_items(self):
        total = 0
        # استخدام related_name للوصول إلى عناصر الطلب
        order_items = self.order_items.all()  # استرجاع جميع عناصر الطلب
        for item in order_items:
            total += item.qty  # جمع الكميات
        return total  # إرجاع المجموع النهائي
    
    def save(self, *args, **kwargs):
        # تعيين الرقم التسلسلي إذا لم يكن موجودًا
        if not self.serial_number:
            last_order = Order.objects.order_by('serial_number').last()
            if last_order:
                # زيادة الرقم التسلسلي بمقدار 1 وتنسيقه ليكون 6 أرقام
                new_serial_number = int(last_order.serial_number) + 1
            else:
                new_serial_number = 1  # إذا لم يكن هناك طلبات سابقة

            # تنسيق الرقم ليكون 6 أرقام
            self.serial_number = str(new_serial_number).zfill(6)  

        super().save(*args, **kwargs)  # استدعاء دالة الحفظ الأساسية

    def __str__(self):
        user_display = self.user.phone_number if self.user else "مستخدم محذوف"
        return f"طلب رقم [{self.serial_number}] من [{user_display}]"

    class Meta:
        verbose_name = 'طلب '
        verbose_name_plural = 'الطلبات'

class OrderItem(models.Model):
    ORDERITEM_STATUS =  [
        ('confirmed', 'مؤكد'),
        ('replaced', 'مُستبدل'),
    ]
    
    status = models.CharField(choices=ORDERITEM_STATUS, max_length=15, default='confirmed', verbose_name='الحالة')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='الطلب')
    order_item = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='order_items' , verbose_name='المنتج')
    qty = models.PositiveIntegerField(default=1, verbose_name='الكمية')
    price = models.PositiveIntegerField(verbose_name='السعر')
    discount_price = models.IntegerField(default=0, verbose_name='الإجمالي بعد الخصم')  # سعر  المنتج بعد الخصم بواسطة الكوبون ان وجد 
    points = models.IntegerField(null=True, verbose_name='المكافأة')
    
    def __str__(self):
        return f"{self.order_item.product_item.product.name}"
 
class OrderDealing(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE , verbose_name='الطلب')
    is_dealt = models.BooleanField(default=False, verbose_name='الاستجابة')
    remaining = models.IntegerField(verbose_name='المتبقي',  default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')
    
    def modifications_numbers(self):
        # حساب عدد DealingItem المرتبطة بـ OrderDealing
        return self.deals.count()

    def calc_remaining(self):
        # حساب المتبقي للطلب
        remaining = 0
        deals = self.deals.filter(is_dealt=False)
        for deal in deals:
            remaining += deal.price_difference if deal.price_difference else 0 
                
        # تحديث الحقل بدون استدعاء save() لتجنب حدوث حلقة لانهائية بسبب الاشارات
        OrderDealing.objects.filter(pk=self.pk).update(remaining=remaining)
    
    def update_order_dealing_dealt(self):
           
        # تحقق من حالة is_dealt لجميع DealingItem المرتبطة
        if all(deal.is_dealt for deal in self.deals.all()):
            self.is_dealt = True
        else:
            self.is_dealt = False

        # حفظ التحديثات
        self.save()

    def __str__(self):
        return f"ملخص تعديلات الطلب {self.order.serial_number} "

    class Meta:
        verbose_name = 'عملية تعديل الطلب'
        verbose_name_plural = 'عمليات تعديل الطلب'
 
class DealingItem(models.Model):
    
    Dealing_status = [
        ('return', 'إرجاع'),
        ('replace', 'إستبدال'),
    ]
    
    order_dealing = models.ForeignKey(OrderDealing, on_delete=models.CASCADE, related_name='deals' , verbose_name='طلب المعالجة')
    old_item = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='old_deals' , verbose_name='المنتج القديم')
    new_item = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='new_deals', null=True, blank=True , verbose_name='المنتج الجديد')
    old_qty = models.IntegerField(null=True, blank=True , verbose_name='الكمية القديمة')
    new_qty = models.IntegerField(null=True, blank=True , verbose_name='الكمية الجديدة')
    old_price = models.IntegerField(default=0, verbose_name='السعر القديم')
    new_price = models.IntegerField(default=0, verbose_name='السعر الجديد')
    price_difference = models.IntegerField(null=True, blank=True , verbose_name='فرق السعر')  
    points_difference =  models.IntegerField(default=0 , verbose_name='فرق النقاط')
    is_dealt = models.BooleanField(default=False , verbose_name='المعالجة') # هل تم تنفيذ عملية التعديل  
    status = models.CharField(max_length=20, choices=Dealing_status, blank=True , verbose_name='الحالة') 
    created_at = models.DateTimeField(auto_now_add=True , verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')
    
    def clean(self):
        if self.status == 'replace':
            if not self.new_item or not self.new_qty:
                raise ValidationError("عند الاستبدال، يجب توفير المنتج الجديد والكمية الجديدة.")
        elif self.status == 'return':
            self.new_item = None
            self.new_qty = None

    def save(self, *args, **kwargs):
        # حفظ DealingItem أولاً
        super().save(*args, **kwargs)
        
        # تحديث total_price_difference و is_dealt في OrderDealing
        self.order_dealing.update_order_dealing_dealt()

    def __str__(self) -> str:
        return f'{self.order_dealing.order.user} => {self.order_dealing.order.serial_number}'
    
    class Meta:
        unique_together = ('order_dealing', 'old_item', 'new_item', 'old_qty', 'new_qty',) # منع إدخال نفس المعاملة مرتين 