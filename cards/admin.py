from django.contrib import admin
from cards.models import *


class CoponAdmin(admin.ModelAdmin):
    list_display = ('copon_image', 'name', 'get_value_display', 'get_price_display', 'sales_count', 'is_active',)
    search_fields = ('name','value',)
    list_filter = ('is_active',)
    ordering = ('sales_count',)   
    exclude = ('sales_count',)
    
    def get_value_display(self, obj):
        return f"{obj.value}$"
    get_value_display.short_description = 'القيمة' # عنوان العمود في الواجهة
    
    def get_price_display(self, obj):
        return f"{obj.price} points"
    get_price_display.short_description = 'السعر' # عنوان العمود في الواجهة
        
class CoponItemAdmin(admin.ModelAdmin):
    list_display = ('get_gift_image', 'get_copon__name', 'user','sell_price', 'get_now_price', 'receive_from_code' ,'has_used', 'expire',)
    search_fields = ('name','value',)
    list_filter = ('has_used','user',)
    ordering = ('-purchase_date',)  
    readonly_fields = ('copon_code', 'user','sell_price', 'get_now_price', 'receive_from_code' ,'has_used', 'purchase_date', 'expire',) 
    
    def get_copon__name(self, obj):
        return f"{obj.copon_code.name}"
    get_copon__name.short_description = ' الكوبون' # عنوان العمود في الواجهة
    
    def get_gift_image(self, obj):
        return f"{obj.copon_code.copon_image()}"
    get_gift_image.short_description = 'الصورة' # عنوان العمود في الواجهة
    
    def get_now_price(self, obj):
        return f"{obj.copon_code.price}"
    get_now_price.short_description = 'السعر الحالي' # عنوان العمود في الواجهة

class ReceiveCoponAdmin(admin.ModelAdmin):
    list_display = ('get_gift_image', 'copon', 'is_used', 'used_by',)
    search_fields = ('copon',)
    list_filter = ('is_used', 'copon')
    ordering = ('updated_at',)   
    readonly_fields = ('code', 'is_used', 'used_by')
    fields = ('copon', 'code', 'is_used', 'used_by', 'note')
    
    def get_gift_image(self, obj):
        return f"{obj.copon.copon_image()}"
    get_gift_image.short_description = 'الصورة' # عنوان العمود في الواجهة
    
    def get_now_price(self, obj):
        return f"{obj.copon_code.price}"
    get_now_price.short_description = 'السعر الحالي' # عنوان العمود في الواجهة
    
admin.site.register(Copon, CoponAdmin)
admin.site.register(CoponItem, CoponItemAdmin)
admin.site.register(ReceiveCopon, ReceiveCoponAdmin)
