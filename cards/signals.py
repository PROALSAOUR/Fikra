from django.db.models.signals import post_save
from django.dispatch import receiver
from cards.models import *
from accounts.models import  UserProfile 
from accounts.send_messages import message_when_buy_gift_for_me, receiver_gift_message, sender_gift_message

@receiver(post_save, sender=GiftItem)
def buy_gift_message(sender, instance, created, **kwargs):
    """دالة تقوم بإرسال رسالة بشكل تلقائي بمجرد شراء هدية """
    if created:  # يتم تنفيذ الكود فقط إذا تم إنشاء عملية شراء جديدة

        profile = UserProfile.objects.get(user=instance.buyer)
        inbox = profile.inbox  # الحصول على صندوق الوارد الخاص بالمشتري
        
        if instance.buyer == instance.recipient:
            # إنشاء رسالة جديدة وإضافتها إلى صندوق الوارد اذا كان المستلم و المشتري نفس الشخص 
            message = message_when_buy_gift_for_me(user_name=instance.buyer.first_name, gift_name=instance.gift)
            inbox.messages.add(message)
            
        else:
            # إنشاء رسالة جديدة وإضافتها إلى صندوق الوارد الخاص بالمشتري والمستلم اذا كان المستلم و المشتري مو نفس الشخص 
            # اولا ارسال رسالة الى المستلم
            re_profile = UserProfile.objects.get(user=instance.recipient)
            re_inbox = re_profile.inbox  
            message = receiver_gift_message(recipient_name=instance.recipient.first_name, buyer_name=instance.buyer, gift_name=instance.gift)
            re_inbox.messages.add(message)
            # ثانيا ارسال رسالة الى المرسل
            se_profile = UserProfile.objects.get(user=instance.buyer)
            se_inbox = se_profile.inbox  
            message = sender_gift_message(user_name=instance.buyer, receiver_name=instance.recipient.first_name, gift_name=instance.gift)
            se_inbox.messages.add(message)


