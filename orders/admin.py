from django.contrib import admin
from orders.models import *

class DliveryPriceAdmin(admin.ModelAdmin):
    list_display = ('price',)
        
    def has_add_permission(self, request, obj=None):
        # السماح بالإضافة فقط إذا لم يكن هناك أي صفحة اسئلة موجودة
        return not DliveryPrice.objects.exists()

class MyOrdersAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status', 'with_message', 'order_date',)
    search_fields = ('user__phone_number',)
    list_filter = ('status', 'with_message',)
    ordering = ('-order_date', '-updated_at',)
    readonly_fields = ('user', 'total_price', 'total_points', 'discount_amount', 'order_date', )
    inlines = []  
    
    
admin.site.register(Order, MyOrdersAdmin)
admin.site.register(DliveryPrice, DliveryPriceAdmin)




