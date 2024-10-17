from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from cards.models import *
from accounts.models import Message, UserProfile 
from django.utils import timezone


@receiver(post_save, sender=GiftItem)
def buy_gift_message(sender, instance, created, **kwargs):
    """دالة تقوم بإرسال رسالة بشكل تلقائي بمجرد شراء هدية """
    if created:  # يتم تنفيذ الكود فقط إذا تم إنشاء عملية شراء جديدة

        profile = UserProfile.objects.get(user=instance.buyer)
        inbox = profile.inbox  # الحصول على صندوق الوارد الخاص بالمشتري
        
        if instance.buyer == instance.recipient:
            # إنشاء رسالة جديدة وإضافتها إلى صندوق الوارد اذا كان المستلم و المشتري نفس الشخص 
            message = Message(
                subject= f'تمت عملية شراء الهدية بنجاح',
                content= 
                f"""
                مرحبا {instance.buyer.first_name}
                لقد تمت عملية شراء الهدية ({ instance.gift }) بنجاح يمكنك العثور عليها الأن داخل مخزونك واستعمالها مع احد طلباتك القادمة ,
                في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن.
                """,
                timestamp=timezone.now()
            )
            
            message.save()
            inbox.messages.add(message)
            
        else:
            # إنشاء رسالة جديدة وإضافتها إلى صندوق الوارد اذا كان المستلم و المشتري مو مفس الشخص 
            
            re_profile = UserProfile.objects.get(user=instance.recipient)
            re_inbox = re_profile.inbox  # الحصول على صندوق الوارد الخاص بالمستخدم
            
            message = Message(
                subject= f' ارسل احدهم هدية اليك!',
                content= 
                f"""
                مرحبا {instance.recipient.first_name}
                لقد قام {instance.buyer} بإرسال هدية [{ instance.gift }]  ,اليك, يمكنك الاطلاع عليها الأن داخل مخزون البطاقات الخاص بك و استعمالها مع اي طلب تريده
                في حال كان لديك اي استفسار يرجى التواصل مع خدمة العملاء وسوف يتم الرد عليك بأسرع وقت ممكن.
                """,
                timestamp=timezone.now()
            )
            
            message.save()
            re_inbox.messages.add(message)
        
# ارسال رساالة عند شراء هدية لشخص ليس لدسه حساب على فكرة

