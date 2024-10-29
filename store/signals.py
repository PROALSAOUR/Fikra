from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductVariation

@receiver(post_save, sender=ProductVariation)
def update_product_sales_count(sender, instance, created, **kwargs):
    """
    دالة تستدعي get_sales_count عند حدوث تغيير في قيمة sold داخل ProductVariation.
    """
    # استدعاء الدالة get_sales_count للمنتج المرتبط بالمتغير
    if instance.sold > 0:  # فقط إذا كانت قيمة sold أكبر من 0
        product = instance.product_item.product
        product.get_sales_count()
