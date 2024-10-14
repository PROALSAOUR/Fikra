from django.db import models
from django.utils.html import mark_safe
from store.models import ProductVariation
from accounts.models import User
       
class DliveryPrice(models.Model):
    price = models.IntegerField(default=0)     
    
    def __str__(self):
        return f"سعر التوصيل {self.price}"
    
    class Meta:
        verbose_name = 'سعر التوصيل '
        verbose_name_plural = 'سعر التوصيل'
        
class Order(models.Model):
    
    ORDER_STATUS = [
        ('pending', 'جاري المعالجة'),
        ('checking', 'جاري التجهيز'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التسليم'),
        ('canceled', 'تم الإلغاء'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    serial_number = models.IntegerField(unique=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    old_total = models.IntegerField()
    total_price = models.PositiveIntegerField()
    total_points = models.PositiveIntegerField(null=True)
    discount_amount = models.IntegerField(default=0)
    dlivery_price = models.IntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    with_message = models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)
    
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
            self.serial_number = str(new_serial_number).zfill(6)  # أو استخدم f"{new_serial_number:06}"

        super().save(*args, **kwargs)  # استدعاء دالة الحفظ الأساسية

    def __str__(self):
        return f"طلب من {self.user} [{self.user.phone_number}]"

    class Meta:
        verbose_name = 'طلب '
        verbose_name_plural = 'الطلبات'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    order_item = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='order_items')
    qty = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()
    returned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.order_item.product_item.product.name}"
    

