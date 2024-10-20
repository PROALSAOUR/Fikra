from django.contrib import admin
from cards.models import *


class CoponAdmin(admin.ModelAdmin):
    list_display = ('copon_image', 'name', 'get_value_display', 'min_bill_price', 'price', 'sales_count', 'is_active',)
    search_fields = ('name','value',)
    list_filter = ('is_active',)
    ordering = ('sales_count',)   
    exclude = ('sales_count',)
    
    def get_value_display(self, obj):
        return f"{obj.value}%"
    get_value_display.short_description = 'القيمة' # عنوان العمود في الواجهة
    
class CoponUsageAdmin(admin.ModelAdmin):
    list_display = ('get_gift_image', 'get_copon__name', 'user','sell_price', 'get_now_price', 'has_used', 'expire',)
    search_fields = ('name','value',)
    list_filter = ('has_used','user',)
    ordering = ('purchase_date',)   
    exclude = ('has_used',)
    
    def get_copon__name(self, obj):
        return f"{obj.copon_code.name}"
    get_copon__name.short_description = ' الكوبون' # عنوان العمود في الواجهة
    
    def get_gift_image(self, obj):
        return f"{obj.copon_code.copon_image()}"
    get_gift_image.short_description = 'الصورة' # عنوان العمود في الواجهة
    
    def get_now_price(self, obj):
        return f"{obj.copon_code.price}"
    get_now_price.short_description = 'السعر الحالي' # عنوان العمود في الواجهة

class GiftAdmin(admin.ModelAdmin):
    list_display = ('gift_image', 'name', 'get_value_display', 'price', 'sales_count', 'is_active',)
    search_fields = ('name','value',)
    list_filter = ('is_active',)
    ordering = ('sales_count',)   
    exclude = ('sales_count',)
    
    def get_value_display(self, obj):
        return f"{obj.value}"
    get_value_display.short_description = 'القيمة' # عنوان العمود في الواجهة

class GiftItemAdmin(admin.ModelAdmin):
    list_display = ('get_gift_image', 'gift__name', 'buyer', 'recipient','sell_value', 'sell_price', 'get_now_price', 'is_seen', 'has_used', 'purchase_date',)
    search_fields = ('gift__name','buyer',)
    list_filter = ('has_used',)
    ordering = ('-purchase_date',)   
    exclude = ('has_used', 'sell_price')
    
    
    def get_gift_image(self, obj):
        return f"{obj.gift.gift_image()}"
    get_gift_image.short_description = 'الصورة' # عنوان العمود في الواجهة
    
    def get_now_price(self, obj):
        return f"{obj.gift.price}"
    get_now_price.short_description = 'السعر الحالي' # عنوان العمود في الواجهة

class GiftDealingAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver_name', 'receiver_phone', 'is_dealt', 'created_at', 'updated_at',)
    search_fields = ('sender',)
    list_filter = ('is_dealt',)
    ordering = ('-created_at',)   
    exclude = ('sender', 'receiver_name', 'receiver_phone',)

class ReceiveGiftAdmin(admin.ModelAdmin):
    list_display = ('get_gift_image' ,'value', 'is_used', 'created_at', 'updated_at')
    search_fields = ('gift__name',)
    list_filter = ('is_used',)
    ordering = ('-updated_at',)   
    exclude = ('is_used', )
    
    
    def get_gift_image(self, obj):
        return f"{obj.gift.gift_image()}"
    get_gift_image.short_description = 'الصورة' # عنوان العمود في الواجهة
    
class GiftmessageAdmin(admin.ModelAdmin):
    list_display = ('gift_item','recipient_name', 'message')
    search_fields = ('recipient_name',)

admin.site.register(Copon, CoponAdmin)
admin.site.register(CoponUsage, CoponUsageAdmin)
admin.site.register(Gift, GiftAdmin)
admin.site.register(GiftItem, GiftItemAdmin)
admin.site.register(GiftDealing, GiftDealingAdmin)
admin.site.register(ReceiveGift, ReceiveGiftAdmin)
admin.site.register(GiftRecipient, GiftmessageAdmin)