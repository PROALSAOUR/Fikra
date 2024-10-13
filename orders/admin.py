from django.contrib import admin
from orders.models import *

class DliveryPriceAdmin(admin.ModelAdmin):
    list_display = ('price',)
        
    def has_add_permission(self, request, obj=None):
        # السماح بالإضافة فقط إذا لم يكن هناك أي صفحة اسئلة موجودة
        return not DliveryPrice.objects.exists()


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # عدم إظهار حقول إضافية
    readonly_fields = ('order_item', 'qty', 'price', )  # جعل الحقول قابلة للقراءة فقط
    can_delete = False  # منع حذف العناصر
    max_num = 0  # منع إضافة عناصر جديدة
    show_change_link = True  

class MyOrdersAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status', 'with_message', 'order_date',)
    search_fields = ('user__phone_number',)
    list_filter = ('status', 'with_message',)
    ordering = ('-order_date', '-updated_at',)
    readonly_fields = ('user', 'old_total', 'discount_amount', 'dlivery_price', 'total_price', 'total_points',  'order_date',  'message',)
    exclude = ('with_message',)
    inlines = [OrderItemInline]  
    
    
admin.site.register(Order, MyOrdersAdmin)
admin.site.register(DliveryPrice, DliveryPriceAdmin)




