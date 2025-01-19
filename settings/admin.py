from django.contrib import admin
from settings.models import Settings, Social

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('settings_file',)
    
    def settings_file(self, obj):
        return "ملف الاعدادات"
    settings_file.short_description = ''
    
    def has_add_permission(self, request, obj=None):
        # السماح بالإضافة فقط إذا لم يكن هناك أي صفحة اسئلة موجودة
        return not Settings.objects.exists()
    
class SocialAdmin(admin.ModelAdmin):
    list_display = ('social_file',)
    
    def social_file(self, obj):
        return "مواقع التواصل "
    social_file.short_description = ''
    
    def has_add_permission(self, request, obj=None):
        # السماح بالإضافة فقط إذا لم يكن هناك أي صفحة اسئلة موجودة
        return not Social.objects.exists()


admin.site.register(Settings, SettingsAdmin)
admin.site.register(Social, SocialAdmin)