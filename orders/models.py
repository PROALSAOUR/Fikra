from django.db import models
from django.utils.html import mark_safe
from store.models import ProductVariation
from accounts.models import User
       
class DliveryPrice(models.Model):
    price = models.IntegerField(default=0)     
    
    def __str__(self):
        return f"طلب من {self.user} [{self.user.phone_number}]"
    
    class Meta:
        verbose_name = 'سعر التوصيل '
        verbose_name_plural = 'سعر التوصيل'
        
class Order(models.Model):
    
    ORDER_STATUS = [
        ('pending', 'جاري المعالجة'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التسليم'),
        ('canceled', 'تم الإلغاء'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    total_price = models.PositiveIntegerField()
    total_points = models.PositiveIntegerField(null=True)
    discount_amount = models.IntegerField(default=0)
    dlivery_price = models.IntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    with_message = models.BooleanField(default=False)
    
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
    

