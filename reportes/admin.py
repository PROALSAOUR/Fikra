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
#========================================================= 
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
#========================================================= 





    

    