from celery import shared_task
from django.utils import timezone
from cards.models import *
from accounts.send_messages import copon_expire_after_3_dayes, copon_expired_today
@shared_task
def check_expire():
    # نحسب تاريخ اليوم ونضيف له 3 أيام
    three_days_from_now = timezone.now().date() + timedelta(days=3)
    copons = CoponItem.objects.filter(has_used=False).select_related('copon_code', 'user__profile__inbox')
    for copon in copons:
        if copon.expire == three_days_from_now : # الكوبونات التي تبقى 3 أيام على صلاحيتها
            inbox = copon.user.profile.inbox  # الوصول المباشر إلى inbox
            # إنشاء الرسالة
            message = copon_expire_after_3_dayes(user_name=copon.user, copon_name=copon.copon_code.name)
            inbox.add_message(message)
        elif copon.is_expire():
            inbox = copon.user.profile.inbox  # الوصول المباشر إلى inbox
            copon.use_copon() # تغيير حالة الكوبون الى مستعمل كي لايتمكن المستخدم من استعماله بعد انتهاء صلاحيته
            # إنشاء الرسالة
            message = copon_expired_today(user_name=copon.user, copon_name=copon.copon_code.name)
            inbox.add_message(message)