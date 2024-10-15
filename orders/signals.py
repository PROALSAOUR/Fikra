from orders.models import Order
from accounts.models import UserProfile, Message
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(pre_save, sender=Order)
def update_user_points(sender, instance, **kwargs):
    try:
        previous_order = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        # إذا كان الطلب جديدًا، لا يوجد حالة سابقة، فنخرج من الدالة
        return

    user_profile = UserProfile.objects.get(user=instance.user)
    user_inbox = user_profile.inbox  # الحصول على صندوق الوارد الخاص بالمستخدم

    # إذا تم تغيير الحالة إلى 'delivered'
    if previous_order.status != 'delivered' and instance.status == 'delivered':
        # إضافة النقاط إلى المستخدم
        user_profile.points += instance.total_points
        user_profile.save()

        # إنشاء رسالة جديدة وإضافتها إلى صندوق الوارد
        message = Message(
            subject= f'تم اضافة نقاط الطلب [{str(instance.serial_number).zfill(6)}] !',
            content= 
            f"""
            مرحبا {instance.user} 
            لقد تمت اضافة النقاط التابعة للطلب [{str(instance.serial_number).zfill(6)}] والتي قيمتها {instance.total_points} نقطة بنجاح الى حسابك, 
            نرجو لك وقتا سعيداً.
            """,
            timestamp=timezone.now()
            )
        message.save()
        user_inbox.messages.add(message)

    elif previous_order.status == 'delivered' and instance.status == 'canceled':
        # خصم النقاط من المستخدم
        user_profile.points -= instance.total_points
        user_profile.save()

        # إنشاء رسالة جديدة وإضافتها إلى صندوق الوارد
        message = Message(
            subject= f'تم خصم نقاط الطلب [{str(instance.serial_number).zfill(6)}] !',
            content= 
            f"""
            مرحبا {instance.user} 
            لقد تم خصم النقاط التابعة للطلب [{str(instance.serial_number).zfill(6)}]  الذي الغيته والتي قيمتها {instance.total_points} نقطة من حسابك, 
            نرجو لك وقتا سعيداً.
            """,
            timestamp=timezone.now()
            )
        message.save()
        user_inbox.messages.add(message)

    user_inbox.save()  # حفظ تحديثات صندوق الوارد