from orders.models import Order, OrderDealing, DealingItem
from accounts.models import UserProfile
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from accounts.send_messages import add_order_points_message
import logging
logger = logging.getLogger(__name__)  # تسجيل الأخطاء في اللوج

@receiver(pre_save, sender=Order)
def update_user_points(sender, instance, **kwargs):
    """تحديث نقاط المستخدم عندما تتحول حالة الطلب من
    مسلم الى ملغي = خصم النقاط
    اي حالة الى مسلم = اضافة النقاط
    """
    try:
        previous_order = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        # إذا كان الطلب جديدًا، لا يوجد حالة سابقة، فنخرج من الدالة
        return
    except Exception as e:
        logger.error(f"خطأ بدالة تحديث نقاط المستخدم داخل اشارات الطلب: {e}", exc_info=True)
        return 
    

    user_profile = UserProfile.objects.get(user=instance.user)
    user_inbox = user_profile.inbox  # الحصول على صندوق الوارد الخاص بالمستخدم

    if previous_order.status != 'delivered' and instance.status == 'delivered':
        # إضافة النقاط إلى المستخدم
        user_profile.points += instance.total_points
        user_profile.save()

        # إنشاء رسالة جديدة وإضافتها إلى صندوق الوارد
        message = add_order_points_message(user_name=instance.user, points=instance.total_points, order=instance)
        message.save()
        user_inbox.add_message(message)

        # إضافة تاريخ التسليم إلى الطلب
        instance.deliverey_date = timezone.now()

    user_inbox.save()  # حفظ تحديثات صندوق الوارد
    
@receiver(post_save, sender=OrderDealing)
def calc_remaining(sender, instance, **kwargs):
    """عند حفظ طلب التعديل تعمل هذه الدالة لحساب متبقي الدفع"""
    instance.calc_remaining()  # تقوم بحساب المتبقي وحفظه
    
@receiver(pre_save, sender=DealingItem)
def update_sold_and_stock(sender, instance, **kwargs):
    """
    دالة تعمل على تحديث كميات المخزون والمباع الخاصة بالمنتج المستبدل او المرجع عندما يسلم الى المستخدم 
    كما انها تنفذ التعديل على نقاط المستخدم ايضا بناءً على فارق السعر 
    """
    try:
        previous_dealing_item = DealingItem.objects.get(pk=instance.pk)
    except DealingItem.DoesNotExist:
        # إذا كان الطلب جديدًا، لا يوجد حالة سابقة، فنخرج من الدالة
        return
    except Exception as e:
        logger.error(f"خطأ بدالة تحديث المُباع و المُخزن داخل اشارات الطلب: {e}", exc_info=True)
        return 
    
    # الدالة تعمل فقط عند تعديل حالة المعالجة الى تمت المعالجة
    if not previous_dealing_item.is_dealt and instance.is_dealt :
        # جلب الكميات والمنتجات (متوافق مع الاستبدال والاسترجاع)
        old_item = instance.old_item
        old_qty = instance.old_qty
        
        old_item.return_product(old_qty)  # إعادة الكمية القديمة إلى المخزون
        
        if instance.status == 'replace': # اذا كانت العملية عملية استبدال قم بتحديث كميات المنتج المستبدل به
            
            new_item = instance.new_item
            new_qty = instance.new_qty
            new_item.sell(new_qty)  # تحديث المبيعات
        
        try:
            order = instance.order_dealing.order
            profile = order.user.profile
            # يتم التحقق ان كان يوجد تاريخ تسليم لأنه قد يكون الطلب سلم ثم ارجعت جميع طلباته فأصبح ملغي
            if order.status == 'delivered' or order.deliverey_date:
                profile.points += instance.points_difference
                profile.save()
        except Exception as e:
            return 
            
    elif  previous_dealing_item.is_dealt and not instance.is_dealt :
        # في حالة قام احدهم بالخطأ بجعل حالة المعالجة صحيحة دون ان تتم المعالجة فعليا
        # ثم اعاد تغير حالة المعالجة الى غير معالجة يتم عكس العملية السابقة تلقائيا هنا
        
        # جلب الكميات والمنتجات (متوافق مع الاستبدال والاسترجاع)
        old_item = instance.old_item
        old_qty = instance.old_qty
        
        old_item.sell(old_qty)  # إعادة الكمية القديمة إلى المخزون
        
        if instance.status == 'replace': # اذا كانت العملية عملية استبدال قم بتحديث كميات المنتج المستبدل به
            
            new_item = instance.new_item
            new_qty = instance.new_qty
            new_item.return_product(new_qty)  # تحديث المبيعات
            
        try:
            order = instance.order_dealing.order
            profile = order.user.profile
            # يتم التحقق ان كان يوجد تاريخ تسليم لأنه قد يكون الطلب سلم ثم ارجعت جميع طلباته فأصبح ملغي
            if order.status == 'delivered' or order.deliverey_date :
                profile.points -= instance.points_difference
                profile.save()
        except Exception as e:
            return 
        
@receiver(pre_save, sender=Order)
def update_sold_and_stock_when_cancel_order(sender, instance, **kwargs):
    "تحديث المخزون للمنتجات داخل الطلب ان كان غير مسلم ثم تم الغائه "
    try:
        order = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        # إذا كان الطلب جديدًا، لا يوجد حالة سابقة، فنخرج من الدالة
        return
    except Exception as e:
        logger.error(f"خطأ بدالة تحديث نقاط المستخدم داخل اشارات الطلب: {e}", exc_info=True)
        return 
    
    # الحالة السابقة تم تغييرها الى ملغي من اي حالة عدا المسلم او الملغي لان هذا يعني ان الحالة لم تتغير
    if order.status != 'delivered' and order.status != 'canceled' and instance.status == 'canceled':
        # لوب على جميع عناصر الطلب يعيدها الى المخزون ويحذفها من المباع
        if order.order_items.exists():
            for order_item in order.order_items.all():
                # جلب الكميات والمنتجات
                item = order_item.order_item
                qty = order_item.qty
                item.return_product(qty)  # إعادة الكمية إلى المخزون
            
@receiver([post_save, post_delete], sender=OrderDealing)
def check_order_dealing_status(sender, instance, **kwargs):
    """
    تحديث حالة الطلب إلى ملغي فقط عندما لا توجد عناصر طلب وجميع عمليات التعديل مكتملة.#
    يعمل فقط ان كانت حالة الطلب السابقة مستلم   #
    # ان كانت حالة الطلب معالجة او تجهيز يتم التعامل من دالة العرض الخاصة بإلغاء عنصر طلب مباشرة
    """

    order = instance.order
    status = order.status

    # تحقق من أنه لا توجد عناصر طلب (OrderItem) مرتبطة بهذا الطلب
    has_order_items = order.order_items.exists()

    # تحقق مما إذا كانت جميع `OrderDealing` الخاصة بهذا الطلب `is_dealt=True`
    all_dealt = not OrderDealing.objects.filter(order=order, is_dealt=False).exists()

    # تغيير الحالة فقط إذا لم يكن هناك عناصر طلب وكل المعاملات مكتملة
    if not has_order_items and all_dealt and status=="delivered":
        order.status = 'canceled'
        order.save()
        
