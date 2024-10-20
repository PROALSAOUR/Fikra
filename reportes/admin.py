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
# دالة عرض الشركاء
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_percent')
    search_fields = ('name',)
    order_by = ('-share_percentage')
    
    def get_percent(self, obj):
        return f"{obj.share_percentage:.2f}%"
    get_percent.short_description = 'النسبة'

    change_list_template = "admin/reportes/partners_changelist.html"  # تخصيص قالب عرض القائمة

    def changelist_view(self, request, extra_context=None):
        # جلب بيانات الشركاء ونسبهم
        partners = Partners.objects.all()
        partner_data = [{"name": partner.name, "share_percentage": float(partner.share_percentage)} for partner in partners]

        extra_context = extra_context or {}
        extra_context['partner_data'] = json.dumps(partner_data)

        return super().changelist_view(request, extra_context=extra_context)
# ========================================================= 
# دالة تكاليف التغليف للطلب الواحد
class PackagingAdmin(admin.ModelAdmin):
    list_display = ('bag_price', 'packaging_paper_price', 'thanks_card_price', 'total')
    readonly_fields = ('total',)
    
    def has_add_permission(self, request, obj=None):
        # السماح بالإضافة فقط إذا لم يكن هناك أي صفحة اسئلة موجودة
        return not Packaging.objects.exists()
# ========================================================= 
class CostInline(admin.TabularInline):
    model = Cost
    extra = 0  
    fields = ('title', 'value', 'description')  # تحديد ترتيب الحقول
    can_delete = True  
    show_change_link = True  
    
class AdditionalInline(admin.TabularInline):
    model = AdditionalIncome
    extra = 0  
    fields = ('title', 'value', 'description')  # تحديد ترتيب الحقول
    can_delete = True  
    show_change_link = True  

class PackForMonthInline(admin.TabularInline):
    model = PackForMonth
    extra = 0  
    fields = ('one_order_packing_cost', )  # تحديد ترتيب الحقول
    can_delete = False  
    max_num = 0
    show_change_link = False  

class MonthlyTotalAdmin(admin.ModelAdmin):
    list_display = ('history', 'total_income', 'show_total_profit' ,'sales_number')
    search_fields = ('history',)
    ordering = ('-month', '-year')
    readonly_fields = ('total_income', 'additional_income', 'total_costs', 'total_packaging', 'goods_price', 'total_profit', 'sales_number',)
    inlines = [CostInline, AdditionalInline, PackForMonthInline]

    def history(self, obj):
        return f'{obj.year}/{obj.month}'
    history.short_description = 'إحصائية شهر'

    def show_total_profit(self, obj):
        if obj.total_profit:
            if obj.total_profit > 0:
                return format_html('<span style="color:#28a745;">{}</span>', obj.total_profit)
            elif obj.total_profit < 0:
                return format_html('<span style="color: red;">{}</span>', obj.total_profit)
            else: # = 0
                return format_html('<span style="color: #e1d221;">{}</span>', obj.total_profit)
        else:
            return '-'
    show_total_profit.short_description = 'الأرباح'

admin.site.register(Partners, PartnersAdmin)
admin.site.register(Packaging, PackagingAdmin)
admin.site.register(MonthlyTotal, MonthlyTotalAdmin)    