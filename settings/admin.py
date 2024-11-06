from django.contrib import admin
from settings.models import Settings

class SettingsAdmin(admin.ModelAdmin):
    list_display = ('settings_file',)
    
    def settings_file(self, obj):
        return "ملف الاعدادات"
    settings_file.short_description = ''
    
    def has_add_permission(self, request, obj=None):
        # السماح بالإضافة فقط إذا لم يكن هناك أي صفحة اسئلة موجودة
        return not Settings.objects.exists()

admin.site.register(Settings, SettingsAdmin)