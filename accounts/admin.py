from django.contrib import admin
from accounts.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone_number')
    search_fields = ('first_name', 'last_name', 'phone_number')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_points')
    search_fields = ('user__phone_number',)
    

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, ProfileAdmin)



