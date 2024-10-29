from celery import shared_task
from datetime import datetime
from reportes.models import *
import decimal
@shared_task
def distribute_profits():
    """
    دالة تحسب ارباح المستثمرين كل شهر   
    """
    
    # احصل على الشهر الحالي
    current_month = datetime.now().month

    # احصل على الاحصائيات التابعة للشهر السابق
    if current_month > 1:
        previous_month = current_month - 1
        year = datetime.now().year
    else:
        previous_month = 12  # في حال كان الشهر الحالي يناير
        year = datetime.now().year - 1
        
    # التأكد من مضي 7 أيام على الشهر الجديد
    if datetime.now().day >= 7:
        # منطق توزيع الأرباح

        month_statis = MonthlyTotal.objects.get(month=previous_month, year=year)
        if month_statis:
            # جلب جميع روابط المجموعات و الاحصائية
            all_monthly_groups = MonthlyInvestmentGroup.objects.filter(monthly_total=month_statis).prefetch_related('investment_group')

            for monthly_group in all_monthly_groups:
                # جيب اجمالي كل مجموعة بالشهر
                monthly_total = monthly_group.total_amount # ربح المجموعة الاجمالي بالشهر
                group = monthly_group.investment_group # جلب المجموعة من الروابط
                all_members = group.members.all() # جيب كل اعضاء المجموعة      
                for member in all_members: 
                    investigator = member.investigator # جلب المستثمر
                    percentage = decimal.Decimal(member.investment_percentage / 100 ) # احسب النسبة
                    # تحقق مما إذا كان هناك توزيع أرباح سابق لهذا الشهر
                    if not InvestigatorProfit.objects.filter(month=month_statis, investigator=investigator, from_group=group).exists():
                    # انشئ ربح مستثمر مرتبط بالشهر 
                        InvestigatorProfit.objects.create(
                            investigator = investigator,
                            month = month_statis,
                            from_group = group,
                            profit = percentage * monthly_total ,
                        )
                    
                    
@shared_task
def add():
    return 9 * 9




