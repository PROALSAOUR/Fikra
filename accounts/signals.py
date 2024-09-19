from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import UserProfile, User, Inbox, Message


@receiver(post_save, sender=User)
def craete_user_profile_and_inbo(sender, instance, created, **kwargs):
    """دالة تقوم بإنشاء بروفايل بشكل تلقائي بمجرد انشاء مستخدم جديد"""
    if created:  # يتم تنفيذ الكود فقط إذا تم إنشاء مستخدم جديد
       # إنشاء صندوق بريد جديد للمستخدم
        inbox = Inbox.objects.create(user=instance)
        # إنشاء بروفايل جديد مرتبط بالمستخدم وصندوق البريد
        UserProfile.objects.create(user=instance, inbox=inbox)
        
