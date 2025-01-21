from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import *
from accounts.send_messages import wellcome_new_user


@receiver(post_save, sender=User)
def craete_user_profile_and_inbo(sender, instance, created, **kwargs):
    """دالة تقوم بإنشاء بروفايل بشكل تلقائي بمجرد انشاء مستخدم جديد"""
    if created:  # يتم تنفيذ الكود فقط إذا تم إنشاء مستخدم جديد
       # إنشاء صندوق بريد جديد للمستخدم
        inbox = Inbox.objects.create(user=instance)
        # إنشاء بروفايل جديد مرتبط بالمستخدم وصندوق البريد
        UserProfile.objects.create(user=instance, inbox=inbox)
            
        # إنشاء رسالة جديدة وإضافتها إلى صندوق الوارد
        message = wellcome_new_user(instance.first_name)
        inbox.add_message(message)
        
@receiver(pre_save, sender=UserProfile)
def track_user_profile_points_change(sender, instance,  **kwargs):
    '''دالة تعمل عند اجراء اي تعديل على البروفايل
    حيث تتحقق من النقاط ان وجدت اي تعديل عليها تنشئ سجل نقاط جديد به القيمة الجديدة والقديمة'''
    
    if instance.pk:
        # نحصل على النسخة القديمة من UserProfile قبل الحفظ
        old_profile = UserProfile.objects.get(pk=instance.pk)
        
        # نتحقق مما إذا كانت النقاط قد تغيرت
        if old_profile.points != instance.points:
            # إذا تغيرت النقاط، ننشئ سجل نقاط جديدًا
            PointsUsage.objects.create(
                user_profile=instance,
                old_points=old_profile.points,
                new_points=instance.points,
                description="تغيير في نقاط المستخدم"
            )


