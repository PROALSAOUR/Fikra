from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import UserProfile, User, Inbox, UserPoints


@receiver(post_save, sender=User)
def craete_user_profile(sender, instance, created, **kwargs):
    """دالة تقوم بإنشاء بروفايل بشكل تلقائي بمجرد انشاء مستخدم جديد"""
    if created:
        UserProfile.objects.create(
            user = instance,     
            user_points=UserPoints.objects.create(user=instance),
            inbox=Inbox.objects.create(user=instance)    
        )