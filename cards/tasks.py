from celery import shared_task
from django.utils import timezone
from cards.models import *
from accounts.send_messages import copon_expire_after_3_dayes, copon_expire_today

@shared_task
def check_expire():
    # نحسب تاريخ اليوم ونضيف له 3 أيام
    three_days_from_now = timezone.now().date() + timedelta(days=3)
    expire_today = timezone.now().date()
        
    cards = CoponUsage.objects.filter(has_used=False).select_related('copon_code', 'user__profile__inbox')
    
    
    for card in cards:
        if card.expire == three_days_from_now : # الكوبونات التي تبقى 3 أيام على صلاحيتها
            inbox = card.user.profile.inbox  # الوصول المباشر إلى inbox
            # إنشاء الرسالة
            message = copon_expire_after_3_dayes(user_name=card.user, copon_name=card.copon_code.name)
            inbox.add_message(message)
        elif card.is_expire():
            inbox = card.user.profile.inbox  # الوصول المباشر إلى inbox
            card.use_copon() # تغيير حالة الكوبون الى مستعمل كي لايتمكن المستخدم من استعماله بعد انتهاء صلاحيته
            # إنشاء الرسالة
            message = copon_expire_today(user_name=card.user, copon_name=card.copon_code.name)
            inbox.add_message(message)
            



