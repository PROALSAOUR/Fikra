from orders.models import Order, OrderDealing
from accounts.models import UserProfile
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from accounts.send_messages import add_order_points_message

@receiver(pre_save, sender=Order)
def update_user_points(sender, instance, **kwargs):
    try:
        previous_order = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        # إذا كان الطلب جديدًا، لا يوجد حالة سابقة، فنخرج من الدالة
        return

    user_profile = UserProfile.objects.get(user=instance.user)
    user_inbox = user_profile.inbox  # الحصول على صندوق الوارد الخاص بالمستخدم

    if previous_order.status != 'delivered' and instance.status == 'delivered':
        # إضافة النقاط إلى المستخدم
        user_profile.points += instance.total_points
        user_profile.save()

        # إنشاء رسالة جديدة وإضافتها إلى صندوق الوارد
        message = add_order_points_message(user_name=instance.user, points=instance.total_points, order_se=instance.serial_number)
        message.save()
        user_inbox.messages.add(message)

        # إضافة تاريخ التسليم إلى الطلب
        instance.deliverey_date = timezone.now()


    user_inbox.save()  # حفظ تحديثات صندوق الوارد
    
@receiver(post_save, sender=OrderDealing)
def calc_remaining(sender, instance, **kwargs):
    """عند حفظ طلب تعديل تعمل هذه الدالة لحساب متبقي الدفع"""
    instance.calc_remaining()  # تقوم بحساب المتبقي وحفظه
    
