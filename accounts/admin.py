from django.contrib import admin
from accounts.models import *
from django.utils.html import format_html

class UserAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_phone_number')
    search_fields = ('first_name', 'last_name', 'phone_number')
    exclude = ('password','email')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'الاسم الكامل'
    
    def get_phone_number(self, obj):
        return f'{obj.phone_number}'
    get_phone_number.short_description = 'رقم الهاتف'

class InboxAdmin(admin.ModelAdmin):
    list_display = ['profile_user', 'phone_number', 'messages_count']
    search_fields = ('userprofile__user__phone_number',)
   
    def profile_user(self, obj):
        return obj.user  # عرض المستخدم المرتبط بصندوق البريد
    profile_user.short_description = 'المستخدم'  # عنوان العمود في الواجهة

    def phone_number(self, obj):
        return obj.user.phone_number
    phone_number.short_description = 'رقم الهاتف' # عنوان العمود في الواجهة
    
    def messages_count(self, obj):
        return obj.messages.count()  # إرجاع عدد الرسائل المرتبطة بصندوق البريد
    messages_count.short_description = 'عدد الرسائل'  # عنوان العمود في الواجهة

class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'timestamp', 'is_read']    
    exclude = ['timestamp', 'is_read']
    
    def get_queryset(self, request):
        """عرض الرسائل المرسلة للجميع فقط"""
        qs = super().get_queryset(request)
        return qs.filter(sent_to_all=True)
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')
    search_fields = ('user__phone_number','user__first_name','user__last_name',)

class PointsUsageAdmin(admin.ModelAdmin):
    list_display = ('user_profile__user', 'old_points', 'new_points', 'get_difference', 'created_at',)
    search_fields = ('user_profile__user', 'user_profile__user__phone_number')
    list_filter = ('user_profile__user',)
    exclude = ['created_at', 'old_points',]
    readonly_fields = ['user_profile', 'old_points', 'new_points', 'created_at',]    # تحديد الحقول التي لا يمكن تعديلها
    
    
    def get_difference(self, obj):
        '''
        دالة تستعمل لإيجاد الفارق بين النقاط القديمة و الجديدة
        '''
        difference = obj.new_points - obj.old_points 
        if difference > 0 : # حدثت زيادة بالنقاط
            return format_html('<span style="color:#28a745; font-weight:900;">+{}</span>', difference)
        elif difference < 0  :  # حدث نقصان بالنقاط
            return format_html('<span style="color: red;">{}</span>', difference)
    get_difference.short_description = 'الفارق' 
    
    def has_delete_permission(self, request, obj=None):
        """منع حذف سجلات النقاط من لوحة الإدارة"""
        return False
    
    def has_add_permission(self, request):
        return False  # يمنع إضافة كائنات جديدة من لوحة الإدارة



admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Inbox, InboxAdmin)
admin.site.register(PointsUsage, PointsUsageAdmin)