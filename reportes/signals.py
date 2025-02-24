from reportes.models import *
from orders.models import Order
from settings.models import Settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import decimal
import logging
logger = logging.getLogger(__name__)  # تسجيل الأخطاء في اللوج
# ترتيب عمل الاشارات الخاصة بالاحصائيات
# 1 update_monthly_totals 
# 2 calc_groups_incomes
# 3 update_partners_profit

# ========================== FUNCTIONS =======================

def get_partners_percentage():
    """دالة تجلب نسبة الشركاء من الربح من ملف الاعدادات"""
    percentage = Settings.objects.values_list('partners_percentage', flat=True).first()
    print(f'persentage is {percentage}++++++++++++++++++++++++++++++++++++++++++')
    return decimal.Decimal(percentage) if percentage else decimal.Decimal(0)

# ========================== SIGNALS =========================

@receiver(post_save, sender=Order)
def update_monthly_totals(sender, created, instance, **kwargs):
    """
    تعمل كلما تم تعديل طلب او انشائه
    تتحقق من حالة الطلب ان كان مسلماً
    تنشئ احصائية شهرية او تعدلها وفقا لتاريخ تسليم الطلب الذي استدعاها
    """
    
    # تحقق انه تم تسليم الطلب    
    if instance.status == 'delivered' and instance.deliverey_date:
                
        # الحصول على الشهر والسنة من تاريخ التسليم الخاص بالطلب
        order = Order.objects.get(id=instance.pk)
        month = order.deliverey_date.month 
        year = order.deliverey_date.year

        #  الحصول على او انشاء احصائية للشهر المطلوب
        monthly_statis, createed = MonthlyTotal.objects.get_or_create(month=month, year=year)
        
        # ========= الحصول على التكاليف الاضافية والمدخلات ============
        
        # التكاليف ان وجدت
        total_costs = sum(cost.value for cost in monthly_statis.costs.all()) if monthly_statis.costs.exists() else 0
        # المدخلات ان وجدت
        additional_income = sum(income.value for income in monthly_statis.incomes.all()) if monthly_statis.incomes.exists() else 0
                                    
        # ========= الحصول على جميع الطلبات المسلمة بنفس الشهر ============
        
        all_orders = Order.objects.filter(
            deliverey_date__month=month, 
            deliverey_date__year=year, 
            status='delivered'
        ).prefetch_related('order_items__order_item__product_item__product')   
        all_orders_count = all_orders.count() 
        # ============== الحصول على المبلغ الاجمالي القادم من بيع المنتجات ===============
        total_income = 0
        for x in all_orders:
            total_income +=  x.total_price
        # ========= الحصول على عدد المنتجات المباعة  خلال الشهر وسعر جملتها  ============
        
        sales_number = 0
        goods_price = 0

        for order in all_orders:
            for item in order.order_items.all():
                sales_number += item.qty
                goods_price += item.qty * item.order_item.product_item.product.purchase_price 
                
        # ================= الحصول على سعر التغليف ==============

        pack, created = PackForMonth.objects.get_or_create(
            for_month=monthly_statis,
            defaults={'one_order_packing_cost': Packaging.objects.first().total if Packaging.objects.exists() else 0}
        )
        
        # الحصول على تكلفة تغلييف جميع الطلبات
        total_packaging = all_orders_count * pack.one_order_packing_cost

        # ================= حساب اجمالي الربح ==============
        
        total_profit = (total_income + additional_income) - ( total_costs + total_packaging + goods_price )

        # ================= تحدييث بيانات الإحصائية الشهرية ==============
        
        monthly_statis.total_income = total_income
        monthly_statis.additional_income = additional_income
        monthly_statis.total_costs = total_costs
        monthly_statis.total_packaging = total_packaging
        monthly_statis.goods_price = goods_price
        monthly_statis.total_profit = total_profit
        monthly_statis.sales_number = sales_number
        
        monthly_statis.save()
        
    else: # اذا لم يكن الطلب مسلما بعد تجاهل كل هذا
        return

@receiver(post_save, sender=MonthlyTotal)
def calc_groups_incomes(sender, created, instance, **kwargs):
    """
    دالة وظيفتها حساب نصيب المجموعات الاستثمارية من المجموع الشهري
    """
    
    # جلب احصائيات الشهر
    total_goods_amount = instance.goods_price or decimal.Decimal(0)  # تعيين قيمة افتراضية
    partners_percentage = get_partners_percentage()  # استدعاء الدالة للحصول على النسبة
    total_profit = decimal.Decimal(instance.total_profit or 0)  # تعيين قيمة افتراضية إذا كان None
    total_profits = total_profit - (total_profit * partners_percentage)  # اجمالي الربح بعد خصم نسبة الشركاء من الربح

    if created: # اذا تم انشاء احصائية قم بإنشاء روابط مجموعات استثمارية
        all_groups = InvestmentGroup.objects.filter(ready=True, completed=False, remaining_amount__gt=0) # جلب جميع المجموعات
    
        if not all_groups: # اذا لم يكن هنالك مجموعات اخرج
            return
        
        #  ايجاد مجموع الحصص لجميع المجموعات
        total_shares = decimal.Decimal(0)
        for group in all_groups:
            total_shares += group.remaining_amount # جلب قيمة الاستثمار المتبقية بكل مجموعة
                
        # ايجاد نسبة كل مجموعة من اجمالي الحصص
        for group in all_groups:
            group_share = group.remaining_amount / total_shares 
            monthly_group , create = MonthlyInvestmentGroup.objects.get_or_create(
                monthly_total= instance,
                investment_group = group,
            )
            monthly_group.monthly_percentage = group_share
            monthly_group.goods_amount = total_goods_amount * group_share
            monthly_group.profit_amount = total_profits * group_share
            monthly_group.total_amount = monthly_group.goods_amount + monthly_group.profit_amount
            monthly_group.save()
            
            # حدث قيمة المتبقي الخاص بكل مجموعة
            group.remaining_amount = group.value # اعد ضبط المتبقي اولا
            group.refund_amount = 0 
            all_group_months = MonthlyInvestmentGroup.objects.filter(investment_group=group) # جلب جميع روابط الشهور بالمجموعة المحددة
            
            for group_month in all_group_months:
                group.remaining_amount -= group_month.goods_amount # ازالة سعر البضاعة التي بيعت من المتبقي
                group.refund_amount += group_month.total_amount # اضافة اجمالي الربح الى العوائد
                group.save() 

    else: 
        # عند تعديل الاستمارة عدل روابط المجموعات الستثمارية فقط
        all_groups_monthly = MonthlyInvestmentGroup.objects.filter(monthly_total=instance) # جلب جميع الروابط
        # جلب المجموعة الخاصة بكل رابط واعادة حساب بياناتها
        for group_monthly in all_groups_monthly:
            # اولا جلب البيانالت الجديدة بعد تعديل الاحصائية
            group_monthly.goods_amount = group_monthly.monthly_percentage *  total_goods_amount
            group_monthly.profit_amount = group_monthly.monthly_percentage * total_profits
            group_monthly.total_amount = group_monthly.goods_amount + group_monthly.profit_amount
            group_monthly.save()
            
            group = group_monthly.investment_group # جلب المجموعة
            group.remaining_amount = group.value # اعادة ضبط قيمة المتبقي
            group.refund_amount = 0 # اعادة ضبط قيمة المتبقي
            all_group_months = MonthlyInvestmentGroup.objects.filter(investment_group=group) # جلب جميع روابط الشهور بالمجموعة المحددة
            for group_month in all_group_months: # اعادة حساب المتبقي
                group.remaining_amount -= group_month.goods_amount # ازالة سعر البضاعة التي بيعت من المتبقي
                group.refund_amount += group_month.total_amount 
                group.save() 

@receiver(post_save, sender=AdditionalIncome)
def handle_additional_income(sender, created, instance, **kwargs):
    """
    تعمل عند انشاء دخل او تعديله وظيفتها تعديل قيم الاحصائية
    """
    #  الحصول على احصائية للشهر المطلوب
    monthly_statis = instance.month
    
    # ========= الحصول على المدخلات ============
    
    additional_income = sum(income.value for income in monthly_statis.incomes.all()) if monthly_statis.incomes.exists() else 0
                                
    # ================= حساب اجمالي الربح ==============
    
    total_profit = (monthly_statis.total_income + additional_income) - ( monthly_statis.total_costs + monthly_statis.total_packaging + monthly_statis.goods_price )

    # ================= تحدييث بيانات الإحصائية الشهرية ==============
    
    monthly_statis.additional_income = additional_income
    monthly_statis.total_profit = total_profit    
    monthly_statis.save()
    
@receiver(post_save, sender=Cost)
def handle_total_costs(sender, created, instance, **kwargs):
    """
    تعمل عند انشاء تكلفة او تعديلها وظيفتها تعديل قيم الاحصائية
    """
    #  الحصول على احصائية للشهر المطلوب
    monthly_statis = instance.month
    
    # ========= الحصول على التكاليف ============
    
    total_costs = sum(cost.value for cost in monthly_statis.costs.all()) if monthly_statis.costs.exists() else 0
                                
    # ================= حساب اجمالي الربح ==============
    
    total_profit = (monthly_statis.total_income + monthly_statis.additional_income) - ( total_costs + monthly_statis.total_packaging + monthly_statis.goods_price )

    # ================= تحدييث بيانات الإحصائية الشهرية ==============
    
    monthly_statis.total_costs = total_costs
    monthly_statis.total_profit = total_profit    
    monthly_statis.save()

@receiver(post_save, sender=PackForMonth)
def handle_total_packaging(sender, created, instance, **kwargs):
    """
    تعمل عند تعديل تكلفة التغليف التابعة للشهر و تعدل قيم الاحصائية
    """
    #  الحصول على احصائية للشهر المطلوب
    monthly_statis = instance.for_month
    
    # ========= الحصول على جميع الطلبات المسلمة بنفس الشهر ============
        
    all_orders = Order.objects.filter(
        deliverey_date__month=monthly_statis.month, 
        deliverey_date__year=monthly_statis.year, 
        status='delivered'
    ).prefetch_related('order_items__order_item__product_item__product')   
    all_orders_count = all_orders.count() 
    
    # الحصول على تكلفة تغلييف جميع الطلبات
    total_packaging = all_orders_count * instance.one_order_packing_cost
                                
    # ================= حساب اجمالي الربح ==============
    
    total_profit = (monthly_statis.total_income + monthly_statis.additional_income) - ( monthly_statis.total_costs + total_packaging + monthly_statis.goods_price )

    # ================= تحدييث بيانات الإحصائية الشهرية ==============
    
    monthly_statis.total_packaging = total_packaging
    monthly_statis.total_profit = total_profit    
    monthly_statis.save()

@receiver(post_save, sender=InvestmentGroupMember)
def update_investment_Group(sender, created, instance, **kwargs):
    """
    دالة وظيفتها تحديث بيانات المجموعة الاستثمارية وايجاد حصتها عند اضافة عضو جديد  
    """
    if created:
        group = instance.group # جلب المجموعة المطلوبة
        
        if not group.ready and not group.completed : # يجب ان تكون المجموعة غير جاهزة ولا مكتملة
        
            group_members = InvestmentGroupMember.objects.filter(group=group)
            
            if group_members:
                group_value = decimal.Decimal(0) 
                
                for member in group_members: # حساب الحصة الاجمالية للمجموعة
                    group_value += member.investment_value 
                    
                group.value = group_value 
                group.remaining_amount = group_value
                group.save()  # حفظ البيانات الجديدة

@receiver(post_save, sender=InvestmentGroup)
def update_Group_members_percentage(sender, created, instance, **kwargs):
    """
    دالة وظيفتها حساب نسبة كل عضو بالمجموعة و حساب عوائده ايضاً
    """ 
    if not created :
        group = instance # جلب المجموعة المطلوبة
        
        group_members = InvestmentGroupMember.objects.filter(group=group)
        if group_members:
            if not group.ready and not group.completed : # يجب ان تكون المجموعة غير جاهزة ولا مكتملة
        
                    group_value = group.value
                    
                    for group_member in group_members: # حساب نسبة كل فرد من المجموعة
                        group_member.investment_percentage = ( group_member.investment_value  / group_value ) * decimal.Decimal(100)
                        group_member.save()
                        
            elif group.ready and group.refund_amount > 0: # في حال كانت المجموعة جاهزة ولديها عوائد
                total_refund = group.refund_amount # جلب عائد المجموعة الاجمالي
                
                for group_member in group_members: # حساب عائد كل فرد من المجموعة وفقا لنسبته
                        group_member.profit_value =  total_refund  * ( group_member.investment_percentage / decimal.Decimal(100) ) # تم تحويل النسبة الى عدد من مئة
                        group_member.save()
                        
@receiver(post_save, sender=MonthlyTotal)
def update_partners_profit(sender, created, instance, **kwargs):
    " دالة وظيفتها حساب ربح الشركاء عند حفظ  احصائية شهرية"
    if instance.total_profit > 0 : # تحقق انه يوجد ربح هذا الشهر
        partners = Partners.objects.all() # جلب جميع الشركاء

        if partners.exists():  # تحقق من وجود الشركاء
            total_profit = decimal.Decimal(instance.total_profit or 0)
            partners_percentage = get_partners_percentage()  # استدعاء الدالة للحصول على النسبة
            total_partners_profit = total_profit * partners_percentage  # جلب نسبة الشركاء الإجمالية من الربح

            for partner in partners:
                partner_profit, created = PartnersProfit.objects.get_or_create(
                    month=instance,
                    partner=partner,
                )
                partner_profit.profit = total_partners_profit * (decimal.Decimal(partner.share_percentage / 100)) # حساب ربح كل شريك
                partner_profit.save()       
                            
@receiver(pre_save, sender=PartnersProfit)
def prevent_received_false(sender, instance, **kwargs):
    """تمنع إعادة تعيين حالة الاستلام لدى الشركاء من مسلم إلى لا."""
    if instance.pk:  # تأكد من أن الكائن موجود (تم إنشاؤه سابقًا)
        try:
            original_instance = PartnersProfit.objects.get(pk=instance.pk)
            if original_instance.received and not instance.received:
                instance.received = True  # استعادة القيمة الأصلية
        except PartnersProfit.DoesNotExist:
            pass 
        except Exception as e:
            logger.error(f"خطأ بالإشارات : {e}", exc_info=True)
            
        
        
@receiver(pre_save, sender=InvestigatorProfit)
def prevent_received_false(sender, instance, **kwargs):
    """تمنع إعادة تعيين حالة الاستلام لدى المستثمرين من مسلم إلى لا."""
    if instance.pk:  # تأكد من أن الكائن موجود (تم إنشاؤه سابقًا)
        try:
            original_instance = InvestigatorProfit.objects.get(pk=instance.pk)
            if original_instance.received and not instance.received:
                instance.received = True  # استعادة القيمة الأصلية
        except InvestigatorProfit.DoesNotExist:
            pass 
        except Exception as e:
            logger.error(f"خطأ بالإشارات : {e}", exc_info=True)
