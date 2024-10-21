from reportes.models import *
from orders.models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Q


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


