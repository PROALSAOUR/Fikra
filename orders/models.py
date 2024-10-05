from django.db import models
from django.utils.html import mark_safe
from store.models import ProductVariation
from accounts.models import User
# Create your models here.
        
class Order(models.Model):
    
    ORDER_STATUS = [
        ('pending', 'جاري المعالجة'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التسليم'),
        ('canceled', 'تم الإلغاء'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    delivery_value = models.PositiveIntegerField(default=0)
    discount_value = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    order_item = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='order_items')
    qty = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

