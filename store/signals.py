from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from store.models import ProductVariation, Product, Interested
from accounts.send_messages import send_message_to_user_when_product_available

@receiver(post_save, sender=ProductVariation)
def update_product_available_and_sales_count(sender, instance, created, **kwargs):
    """
    دالة تستدعي get_sales_count عند حدوث تغيير في قيمة sold داخل ProductVariation.
    """
    # استدعاء الدالة get_sales_count للمنتج المرتبط بالمتغير
    if instance.sold > 0:
        product = instance.product_item.product
        product.get_sales_count()
        
    """
    دالة تقوم بتحديث قيمة متوفر داخل المنتج عند التعديل على كميات stock 
    """
    product = instance.product_item.product
    product.available = True if product.get_total_stock() > 0 else False
    product.save()

@receiver(pre_save, sender=Product)
def tell_user_when_product_available(sender, instance, **kwargs):
    """
    ارسال رسالة الى المستخدم عند توفر االمنتج الذي كان مهتما به 
    """        
    if instance.pk:  # التحقق مما إذا كان المنتج موجودًا مسبقًا
        previous = Product.objects.filter(pk=instance.pk).first()
        if previous and not previous.available and instance.available:
            # جلب المستخدمين المهتمين بهذا المنتج
            interested_users = Interested.objects.filter(product=instance).select_related('user')
            for interest in interested_users:
                user = interest.user
                message = send_message_to_user_when_product_available(user_name=user.first_name, product_name=instance.name, product_id=instance.id)
                inbox = user.profile.inbox
                inbox.add_message(message)
                inbox.save()
            interested_users.delete() # حذف الاهتمامات بعد إرسال الإشعارات