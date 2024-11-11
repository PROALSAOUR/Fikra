from django.db import models
from django.utils.html import mark_safe
from store.models import ProductVariation
from django.core.exceptions import ValidationError
from accounts.models import User
       
class DliveryPrice(models.Model):
    price = models.IntegerField(default=0 , verbose_name='سعر التوصيل')     
    
    def __str__(self):
        return f"سعر التوصيل {self.price}"
    
    class Meta:
        verbose_name = 'سعر التوصيل '
        verbose_name_plural = 'سعر التوصيل'
        
class Order(models.Model):
    
    ORDER_STATUS = [
        ('pending', 'جاري المعالجة'),
        ('checking', 'جاري التجهيز'),
        ('shipped', 'جاري الشحن'),
        ('delivered', 'تم التسليم'),
        ('canceled', 'تم الإلغاء'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders' , verbose_name='المستخدم')
    serial_number = models.IntegerField(unique=True, verbose_name='الرقم التسلسلي')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending' , verbose_name='الحالة')
    old_total = models.IntegerField(verbose_name='الإجمالي القديم')
    total_price = models.PositiveIntegerField(verbose_name='الإجمالي')
    total_points = models.PositiveIntegerField(null=True, verbose_name='المكافأة')
    discount_amount = models.IntegerField(default=0, verbose_name='قيمة الخصم')
    dlivery_price = models.IntegerField(default=0, verbose_name='سعر التوصيل')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الطلب')
    deliverey_date = models.DateTimeField(null=True, blank=True, verbose_name='تاريخ التسليم')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')
    with_message = models.BooleanField(default=False, verbose_name='مع رسالة؟')
    message = models.TextField(blank=True, null=True, verbose_name='الرسالة')
        
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
        return f"طلب رقم [{self.serial_number}] من [{self.user.phone_number}]"

    class Meta:
        verbose_name = 'طلب '
        verbose_name_plural = 'الطلبات'

class OrderItem(models.Model):
    ORDERITEM_STATUS =  [
        ('confirmed', 'مؤكد'),
        ('replaced', 'مُستبدل'),
    ]
    
    status = models.CharField(choices=ORDERITEM_STATUS, max_length=15, default='confirmed')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='الطلب')
    order_item = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='order_items' , verbose_name='المنتج')
    qty = models.PositiveIntegerField(default=1, verbose_name='الكمية')
    price = models.PositiveIntegerField(verbose_name='السعر')
    points = models.IntegerField(null=True, verbose_name='المكافأة')
    
    def __str__(self):
        return f"{self.order_item.product_item.product.name}"
 
class OrderDealing(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE , verbose_name='الطلب')
    is_dealt = models.BooleanField(default=False, verbose_name='الاستجابة')
    total_price_difference = models.IntegerField(default=0, null=True , verbose_name='فرق السعر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التعديل')
    
    def update_total_price_difference_and_is_dealt(self):
        # لأنو اذا ما كان مستلم لسا مافي داعي نعمل تغيير بالسعر لأنو اصلا مادفع
        if self.order.status == 'delivered' :  
            # حساب مجموع price_difference لجميع DealingItem المرتبطة
            total_price_diff = sum(
                deal.price_difference for deal in self.deals.all() 
                if deal.price_difference is not None and not deal.is_dealt
            )
            self.total_price_difference = total_price_diff
                   
        # تحقق من حالة is_dealt لجميع DealingItem المرتبطة
        if all(deal.is_dealt for deal in self.deals.all()):
            self.is_dealt = True
        else:
            self.is_dealt = False

        # حفظ التحديثات
        self.save()

    def modifications_numbers(self):
        # حساب عدد DealingItem المرتبطة بـ OrderDealing
        return self.deals.count()
    
    def save(self, *args, **kwargs):
        if self.order.status != 'delivered':
            self.total_price_difference = None
        super().save(*args, **kwargs)

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
    price_difference = models.IntegerField(null=True, blank=True , verbose_name='فرق السعر')  
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
        self.order_dealing.update_total_price_difference_and_is_dealt()

    def __str__(self) -> str:
        return f'{self.order_dealing.order.user} => {self.order_dealing.order.serial_number}'
    