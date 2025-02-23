from django.contrib import admin
from django.http import HttpRequest
from reportes.models import *
from accounts.models import User
from orders.models import Order
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek, ExtractDay
from django.template.response import TemplateResponse
from django.utils import timezone
import json
from django.utils.html import format_html

# ======================================================================================================================
# ازالة  django_beat_celery من لوحة الادارة
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule
# حاول إلغاء تسجيل كل نموذج على حدة إذا كان مسجلاً مسبقًا
for model in [PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule]:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass
# ======================================================================================================================

# دالة عدد المستخدمين الاجمالي
@admin.register(UserReports)
class UserReportsAdmin(admin.ModelAdmin):
      
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    def has_change_permission(self, request: HttpRequest, obj=None ) -> bool:
        return False
    
    change_list_template = 'admin/reportes/users-count.html'  
    
    def changelist_view(self, request, extra_context=None) :
        now = timezone.now() 
        
        yearly_stats = (
            User.objects
            .annotate(year=ExtractYear('date_joined')) 
            .values('year')
            .annotate(user_count=Count('id'))
            .order_by('year')
        )
        
        # حساب العدد التراكمي للحسابات حتى كل سنة
        yearly_cumulative_counts = []
        yearly_cumulative_sum = 0

        for stat in yearly_stats:
            yearly_cumulative_sum += stat['user_count']
            yearly_cumulative_counts.append({
                'year': stat['year'],
                'user_count': yearly_cumulative_sum,
            })
        
        
        monthly_stats = (
            User.objects
            .annotate(year=ExtractYear('date_joined'))
            .annotate(month=ExtractMonth('date_joined'))
            .values('year', 'month')
            .annotate(user_count=Count('id'))
            .order_by('year', 'month')[:30]
        )
        

        # حساب العدد التراكمي للحسابات حتى كل شهر
        monthly_cumulative_counts = []
        monthly_cumulative_sum = 0

        for stat in monthly_stats:
            monthly_cumulative_sum += stat['user_count']
            monthly_cumulative_counts.append({
                'year': stat['year'],
                'month': stat['month'],
                'user_count': monthly_cumulative_sum,
            })
        
        
        weekly_stats = (
            User.objects
            .annotate(year=ExtractYear('date_joined'))
            .annotate(week=ExtractWeek('date_joined'))
            .filter(date_joined__lte=now)
            .values('year', 'week')
            .annotate(user_count=Count('id'))
            .order_by('year', 'week')[:30]
        )
        
        # حساب العدد التراكمي للحسابات حتى كل أسبوع
        weekly_cumulative_counts = []
        weekly_cumulative_sum = 0

        for stat in weekly_stats:
            weekly_cumulative_sum += stat['user_count']
            weekly_cumulative_counts.append({
                'year': stat['year'],
                'week': stat['week'],
                'user_count': weekly_cumulative_sum,
            })
        
        
        context = {
            **self.admin_site.each_context(request),    
            'yearly_stats': json.dumps(list(yearly_cumulative_counts)),
            'monthly_stats': json.dumps(list(monthly_cumulative_counts)),
            'weekly_stats': json.dumps(list(weekly_cumulative_counts)),
        }
        total_users = User.objects.count()
        context['total_users'] = total_users
        
        return TemplateResponse(request, self.change_list_template, context)
# ========================================================= 
# دالة عدد الطلبات
@admin.register(OrdersCount)
class OrdersCountAdmin(admin.ModelAdmin):
      
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    def has_change_permission(self, request: HttpRequest, obj=None ) -> bool:
        return False
    
    change_list_template = 'admin/reportes/orders-count.html'  
    
    def changelist_view(self, request, extra_context=None):
        now = timezone.now()

        # Querysets الخاصة بجلب البيانات
        yearly_stats = (
            Order.objects
            .annotate(year=ExtractYear('order_date'))
            .values('year', 'status')  # تجميع الطلبات بناءً على السنة والحالة
            .annotate(order_count=Count('id'))
            .order_by('year')
        )

        monthly_stats = (
            Order.objects
            .annotate(year=ExtractYear('order_date'))
            .annotate(month=ExtractMonth('order_date'))
            .values('year', 'month', 'status')  # تجميع الطلبات بناءً على السنة، الشهر، والحالة
            .annotate(order_count=Count('id'))
            .order_by('year', 'month')
        )

        weekly_stats = (
            Order.objects
            .annotate(year=ExtractYear('order_date'))
            .annotate(week=ExtractWeek('order_date'))
            .values('year', 'week', 'status')  # تجميع الطلبات بناءً على السنة، الأسبوع، والحالة
            .annotate(order_count=Count('id'))
            .order_by('year', 'week')
        )
        
        daily_stats = (
            Order.objects
            .annotate(year=ExtractYear('order_date'))
            .annotate(month=ExtractMonth('order_date'))
            .annotate(day=ExtractDay('order_date'))  # استخراج اليوم من تاريخ الطلب
            .values('year', 'month', 'day', 'status')  # تجميع الطلبات بناءً على السنة، الشهر، اليوم، والحالة
            .annotate(order_count=Count('id'))  # عدّ الطلبات لكل يوم وحالة
            .order_by('year', 'month', 'day')[:30]  # الحصول على آخر 30 يومًا
        )


        context = {
            **self.admin_site.each_context(request),
            'yearly_stats': json.dumps(list(yearly_stats)),
            'monthly_stats': json.dumps(list(monthly_stats)),
            'weekly_stats': json.dumps(list(weekly_stats)),
            'daily_stats': json.dumps(list(daily_stats)),  # إضافة البيانات اليومية إلى الـ context

        }

        return TemplateResponse(request, self.change_list_template, context)
# ========================================================= 
# دالة ربح الشركاء
class PartnersProfitInline(admin.TabularInline):
    model = PartnersProfit
    extra = 0  
    max_num = 0
    readonly_fields = ('month', 'profit', )  
    fields = ('month', 'profit', "received") 
    ordering = ('month',) 
    can_delete = False  
    show_change_link = False 
        
# دالة الشركاء
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'get_percent')
    search_fields = ('name', 'phone_number',)
    order_by = ('-share_percentage')
    inlines = [PartnersProfitInline,]
    
    def get_percent(self, obj):
        return f"{obj.share_percentage:.2f}%"
    get_percent.short_description = 'النسبة'

    change_list_template = "admin/reportes/partners.html"  # تخصيص قالب عرض القائمة

    def changelist_view(self, request, extra_context=None):
        # جلب بيانات الشركاء ونسبهم
        partners = Partners.objects.all()
        partner_data = [{"name": partner.name, "share_percentage": float(partner.share_percentage)} for partner in partners]

        extra_context = extra_context or {}
        extra_context['partner_data'] = json.dumps(partner_data)

        return super().changelist_view(request, extra_context=extra_context)

# دالة ربح المستثمرين
class InvestigatorProfitInline(admin.TabularInline):
    model = InvestigatorProfit
    extra = 0  
    max_num = 0
    readonly_fields = ('month', 'from_group', 'profit', )  
    fields = ('month', 'from_group', 'profit', "received")  
    ordering = ('month',)
    can_delete = False  
    show_change_link = False 
    
# دالة عرض المستثمرين
class InvestigatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', )
    search_fields = ('name', 'phone_number',)
    inlines = [InvestigatorProfitInline,]

# دالة اعضاءالمجموعة الاستثمارية
class GroupMembersInline(admin.TabularInline):
    model = InvestmentGroupMember
    extra = 0  
    fields = ('investigator', 'investment_value', "show_percentage", 'profit_value', 'created_at', )  
    readonly_fields = ('show_percentage', 'profit_value', 'created_at', )  
    can_delete = True  
    show_change_link = True 
        
    def show_percentage(self,  obj=None):
        '''تضيف علامة النسبة المئوية بجانب نسبة العضو'''
        if obj: 
            return f"{obj.investment_percentage}%"
        return "-"
    show_percentage.short_description = "النسبة"

        
    def get_readonly_fields(self,request , obj=None):
        """منع اضافة اعضاء اذا كانت حالة المجموعة جاهزة او مكتملة"""
        if obj and obj.ready  :
            self.show_change_link=False 
            self.can_delete=False 
            self.max_num = 0
            return self.readonly_fields + ('investigator', 'investment_value', "show_percentage", 'profit_value', 'created_at', ) 
        return self.readonly_fields
    
#  دالة عرض المجموعات الستثمارية
class InvestmentGroupAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'value', 'remaining_amount' ,'refund_amount', 'ready', 'completed')
    search_fields = ('name',)
    list_filter = ('completed',)
    ordering = ('-created_at', '-updated_at')
    fields = ('name', 'value', 'remaining_amount', 'refund_amount', 'completed', 'ready' )
    readonly_fields = ('value', 'remaining_amount', 'refund_amount', 'completed',)
    inlines = [GroupMembersInline,]
    
    def get_readonly_fields(self, request, obj=None):
        """منع تعديل حالة الجهوزية اذا كانت حالة المجموعة جاهزة  """
        if obj and obj.ready :
            return self.readonly_fields + ('ready',) 
        return self.readonly_fields

# ========================================================= 

# دالة تكاليف التغليف للطلب الواحد
class PackagingAdmin(admin.ModelAdmin):
    list_display = ('bag_price', 'packaging_paper_price', 'thanks_card_price', 'total')
    readonly_fields = ('total',)
    
    def has_add_permission(self, request, obj=None):
        # السماح بالإضافة فقط إذا لم يكن هناك أي صفحة اسئلة موجودة
        return not Packaging.objects.exists()

# ========================================================= 
# قيمة المصاريف داخل الاحصائية 
class CostInline(admin.TabularInline):
    model = Cost
    extra = 0  
    fields = ('title', 'value', 'description')  # تحديد ترتيب الحقول
    can_delete = True  
    show_change_link = True  
    
    def is_latest(self, obj):
        latest = MonthlyTotal.objects.order_by('-year', '-month').first()
        return obj == latest

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        if obj and not self.is_latest(obj):
            readonly += ('title', 'value', 'description')
        return readonly
# قيمة الاضافات داخل الاحصائية 
class AdditionalInline(admin.TabularInline):
    model = AdditionalIncome
    extra = 0  
    fields = ('title', 'value', 'description')  # تحديد ترتيب الحقول
    can_delete = True  
    show_change_link = True  
    
    # لمنع التعديل ان كانت هذه احصائية قديمة
    def is_latest(self, obj):
        latest = MonthlyTotal.objects.order_by('-year', '-month').first()
        return obj == latest

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        if obj and not self.is_latest(obj):
            readonly += ('title', 'value', 'description')
        return readonly
# سعر تغليف الطلب الواحد داخل الاحصائية
class PackForMonthInline(admin.TabularInline):
    model = PackForMonth
    extra = 0  
    fields = ('one_order_packing_cost', )  # تحديد ترتيب الحقول
    can_delete = False  
    max_num = 0
    show_change_link = False  
    
    
    # لمنع التعديل ان كانت هذه احصائية قديمة
    def is_latest(self, obj):
        latest = MonthlyTotal.objects.order_by('-year', '-month').first()
        return obj == latest

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        if obj and not self.is_latest(obj):
            readonly +=  ('one_order_packing_cost', )  
        return readonly
# ارباح الشركاء داخل الاحصائية الشهرية
class MonthPartnersProfitInline(admin.TabularInline):
    model = PartnersProfit
    extra = 0  
    max_num = 0
    readonly_fields = ('partner', 'profit', "received")    
    can_delete = False  
    show_change_link = False 
# دالة ربح المجموعات دالة الاحصائية
class MonthlyInvestmentGroupInline(admin.TabularInline):
    model = MonthlyInvestmentGroup
    extra = 0  # عدد الصفوف الإضافية
    max_num = 0
    readonly_fields = ('monthly_total', 'investment_group', "monthly_percentage", 'goods_amount', 'profit_amount', 'total_amount')    
    can_delete = False  
    show_change_link = False 
    verbose_name_plural = 'الاستثمارات'
# دالة عرض الاحصائية الرئيسية
class MonthlyTotalAdmin(admin.ModelAdmin):
    list_display = ('history', 'colored_total_income', 'colored_total_profit' ,'sales_number')
    search_fields = ('history',)
    ordering = ('-year', '-month', )
    fields = ('history', 'colored_total_income', 'colored_additional_income', 'colored_total_costs', 'colored_total_packaging', 'colored_goods_price', 'colored_total_profit', 'sales_number',)
    readonly_fields = ('history', 'colored_total_income', 'colored_additional_income', 'colored_total_costs', 'colored_total_packaging', 'colored_goods_price', 'colored_total_profit', 'sales_number',)
    exclude = ('total_income', 'additional_income', 'total_costs', 'total_packaging', 'goods_price','total_profit', 'month', 'year')
    inlines = [CostInline, AdditionalInline, PackForMonthInline, MonthPartnersProfitInline, MonthlyInvestmentGroupInline]

    def colored_total_income(self, obj):
        if obj.total_income:
            if obj.total_income > 0:
                return format_html('<span style="color:#28a745;">+{}</span>', obj.total_income)
        else:
            return '0'
    colored_total_income.short_description = ' الدخل'
    
    def colored_additional_income(self, obj):
        if obj.additional_income:
            if obj.additional_income > 0:
                return format_html('<span style="color:#28a745;">+{}</span>', obj.additional_income)
        else:
            return '0'
    colored_additional_income.short_description = 'الإضافات'

    def colored_total_costs(self, obj):
        if obj.total_costs:
            if obj.total_costs > 0:
                return format_html('<span style="color:red;">-{}</span>', obj.total_costs)
        else:
            return '0'
    colored_total_costs.short_description = 'المصاريف'

    def colored_total_packaging(self, obj):
        if obj.total_packaging:
            if obj.total_packaging > 0:
                return format_html('<span style="color:red;">-{}</span>', obj.total_packaging)
        else:
            return '0'
    colored_total_packaging.short_description = 'التغليف'

    def colored_goods_price(self, obj):
        if obj.goods_price:
            if obj.goods_price > 0:
                return format_html('<span style="color:red;">-{}</span>', obj.goods_price)
        else:
            return '0'
    colored_goods_price.short_description = 'سعر البضاعة'

    def colored_total_profit(self, obj):
        if obj.total_profit:
            if obj.total_profit > 0:
                return format_html('<span style="color:#28a745;">+{}</span>', obj.total_profit)
            elif obj.total_profit < 0:
                return format_html('<span style="color: red;">{}</span>', obj.total_profit)
            else: # = 0
                return format_html('<span style="color: #e1d221;">{}</span>', obj.total_profit)
        else:
            return '-'
    colored_total_profit.short_description = 'الأرباح'
    
    def history(self, obj):
        return f'{obj.year}/{obj.month}'
    history.short_description = 'إحصائية شهر'

    def is_latest(self, obj):
        latest = MonthlyTotal.objects.order_by('-year', '-month').first()
        return obj == latest

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        if obj and not self.is_latest(obj):
            readonly += ('total_income', 'additional_income', 'total_costs', 'total_packaging', 'goods_price', 'total_profit')
        return readonly
    

    change_list_template = "admin/reportes/monthly-statis.html"  
    def changelist_view(self, request, extra_context=None):
        # جلب جميع البيانات الخاصة بالأرباح مرتبة حسب السنة والشهر
        unsorted_profit_data = (
            MonthlyTotal.objects
            .values('year', 'month', 'total_profit', 'sales_number')
            .order_by('-year', '-month')[:24]  # اخذ اخر 24 شهر فقط
        )
        # ترتيب الشهور من الاصغر الى الاكبر
        profit_data =  sorted(unsorted_profit_data, key=lambda x: (x['year'], x['month']))

        # إعداد البيانات للرسم البياني
        months = [f"{item['year']}/{item['month']}" for item in profit_data]
        profits = [float(item['total_profit']) if item['total_profit'] else 0 for item in profit_data]
        sales = [item['sales_number'] if item['sales_number'] else 0 for item in profit_data]

        # إضافة شهر جديد مع قيم صفر
        if months:  # تأكد من وجود بيانات
            last_month = months[0]
            year, month = map(int, last_month.split('/'))
            previous_month = f"{year}/{month - 1 if month > 1 else 12}"  # الشهر السابق

            # إضافة الشهر السابق إلى البيانات
            months.insert(0, previous_month)
            profits.insert(0, 0)  # قيمة الربح
            sales.insert(0, 0)  # عدد المبيعات

        # تمرير البيانات إلى الـ context
        extra_context = extra_context or {}
        extra_context['profit_data'] = json.dumps({
            'months': months,
            'profits': profits,
            'sales': sales,
        })

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Partners, PartnersAdmin)
admin.site.register(Investigator, InvestigatorAdmin)
admin.site.register(Packaging, PackagingAdmin)
admin.site.register(MonthlyTotal, MonthlyTotalAdmin)    
admin.site.register(InvestmentGroup, InvestmentGroupAdmin)