from django.contrib import admin
from accounts.models import *
from accounts.forms import SendMessageForm


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

class MessageInline(admin.TabularInline):
    model = Inbox.messages.through
    extra = 1  # عدد النماذج الفارغة التي ستظهر افتراضيًا
    fields = ('message',)  # الحقول التي تريد عرضها في النموذج الفرعي
    verbose_name = 'رسالة'
    verbose_name_plural = 'رسائل'

class InboxAdmin(admin.ModelAdmin):
    list_display = ['profile_user', 'messages_count']
    search_fields = ('profile__user__phone_number',)
    inlines = [MessageInline]
   
    def profile_user(self, obj):
        return obj.user  # عرض المستخدم المرتبط بصندوق البريد
    profile_user.short_description = 'المستخدم'  # عنوان العمود في الواجهة

    def messages_count(self, obj):
        return obj.messages.count()  # إرجاع عدد الرسائل المرتبطة بصندوق البريد
    messages_count.short_description = 'عدد الرسائل'  # عنوان العمود في الواجهة

class SendMessageAdmin(admin.ModelAdmin):
    form = SendMessageForm
    list_display = ['subject', 'timestamp']
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')
    search_fields = ('user__phone_number','user__first_name','user__last_name',)
    
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Message, SendMessageAdmin)
admin.site.register(Inbox, InboxAdmin)


