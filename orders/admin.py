from django.contrib import admin
from django.utils.html import format_html
from orders.models import *

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # عدم إظهار حقول إضافية
    readonly_fields = ('get_product_image', 'order_item', 'qty', 'price', 'get_total', 'discount_price',)  # جعل الحقول قابلة للقراءة فقط
    fields = ('get_product_image', 'order_item',  'qty', 'price', 'get_total', 'discount_price', 'status', )  # تحديد ترتيب الحقول
    can_delete = False  # منع حذف العناصر
    max_num = 0  # منع إضافة عناصر جديدة
    show_change_link = True  
    verbose_name_plural = 'عناصر الطلب'
    
    def get_total(self, obj):
        if obj.qty is not None and obj.price is not None:
            return obj.qty * obj.price
        return 0 
    get_total.short_description = 'الإجمالي'  
    
    def get_product_image(self, obj):
        # التأكد من وجود صورة مرتبطة بعنصر المنتج
        if obj.order_item and obj.order_item.product_item.image:
            return mark_safe("<img src='%s' width='50' height='50' />" % (obj.order_item.product_item.image.url))
        return "No Image"
    get_product_image.short_description = 'الصورة' 
    
class OrderDealingInline(admin.TabularInline):
    model = OrderDealing
    extra = 0  # عدم إظهار حقول إضافية
    readonly_fields = ('get_dealing_items_number', 'get_dealt_items_number', 'get_not_dealt_items_number', 'is_dealt', 'remaining' )  # جعل الحقول قابلة للقراءة فقط
    fields = ('get_dealing_items_number', 'get_dealt_items_number', 'get_not_dealt_items_number', 'is_dealt', 'remaining' )  # تحديد ترتيب الحقول
    can_delete = False  # منع حذف العناصر
    max_num = 0  # منع إضافة عناصر جديدة
    show_change_link = True  
    verbose_name_plural = 'التعديلات '
     
    def get_dealing_items_number(self, obj):
        """تعيد عدد التعديلات الاجمالي التابعة للطلب"""
        return obj.modifications_numbers()
    get_dealing_items_number.short_description = "عدد التعديلات"
    
    def get_dealt_items_number(self, obj):
        """تعيد عدد التعديلات  المعالجة التابعة للطلب""" 
        return obj.deals.filter(is_dealt=True).count()
    get_dealt_items_number.short_description = "المعالجة"
    
    def get_not_dealt_items_number(self, obj):
        """تعيد عدد التعديلات الغير معالجة التابعة للطلب"""
        return obj.deals.filter(is_dealt=False).count()
    get_not_dealt_items_number.short_description = "المتبقية"
    
class MyOrdersAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'get_user', 'total_price', 'colored_status',  'order_date',)
    search_fields = ('serial_number', 'user__phone_number',)
    list_filter = ('status', 'user__phone_number', 'city',)
    ordering = ('-order_date', '-updated_at',)
    fields = ( 'user', 'status', 'serial_number',  'old_total', 'used_discount', 'total_price', 'copon_value', 'total_points', 'free_delivery', 'city', 'neighborhood', 'order_date', 'deliverey_date', )
    readonly_fields = ( 'user', 'serial_number',  'old_total', 'used_discount', 'total_price', 'copon_value', 'total_points', 'free_delivery', 'order_date', 'deliverey_date', )
    inlines = [OrderItemInline, OrderDealingInline] 
    
    def get_readonly_fields(self, request, obj=None):
        """جعل حقل الحالة غير قابل للتعديل إذا كانت الحالة مُلغاة."""
        if obj and obj.status == 'canceled':
            return self.readonly_fields + ('status',)
        return self.readonly_fields
    
    def get_user(self,obj):
        return obj.user if obj.user else "مستخدم محذوف"
    get_user.short_description = "المستخدم"
    
    def colored_status(self, obj):
        """إرجاع الحالة مع تلوين خاص بناءً على القيمة."""
        if obj.status == 'canceled':
            return format_html('<span style="color: red;">{}</span>', obj.get_status_display())
        elif obj.status == 'delivered':
            return format_html('<span style="color:#28a745; font-weight:900;">{}</span>', obj.get_status_display())
        elif obj.status == 'shipped':
             return format_html('<span style="color:#215ee1; font-weight:900;">{}</span>', obj.get_status_display())
        elif obj.status == 'checking':
             return format_html('<span style="color:#ff7623; font-weight:900;">{}</span>', obj.get_status_display())
        else: # status = pending
            return format_html('<span style="color:#e1d221; font-weight:900;">{}</span>', obj.get_status_display())
    colored_status.short_description = 'الحالة'   

    def has_add_permission(self, request):
        return False  # يمنع إضافة كائنات جديدة من لوحة الإدارة

class DealingItemsInline(admin.TabularInline):
    model = DealingItem
    extra = 0  # عدم إظهار حقول إضافية
    readonly_fields = ('old_item', 'new_item', 'old_qty', 'new_qty', 'price_difference', 'status', ) 
    fields = ('old_item', 'new_item', 'old_qty', 'new_qty', 'price_difference', 'is_dealt', 'status' )  # تحديد ترتيب الحقول
    can_delete = False  # منع حذف العناصر
    max_num = 0  # منع إضافة عناصر جديدة
    show_change_link = True  
    
class DealingAdmin(admin.ModelAdmin):
    list_display = ('order__user', 'order', 'status', 'get_modifications', 'is_dealt', 'created_at', )    
    search_fields = ('order__user__phone_number', )
    list_filter = ('order', 'is_dealt',)
    ordering = ('is_dealt', '-updated_at', '-created_at',)
    readonly_fields = ( 'order', 'remaining', 'created_at', 'updated_at',)
    inlines = [DealingItemsInline] 
    
    def get_modifications(self, obj):
        return obj.modifications_numbers()
    get_modifications.short_description = 'التعديلات'
  
    def status(self, obj):
        """إرجاع الحالة مع تلوين خاص بناءً على القيمة."""
        if obj.order.status == 'canceled':
            return format_html('<span style="color: red;">{}</span>', obj.order.get_status_display())
        elif obj.order.status == 'delivered':
            return format_html('<span style="color:#28a745; font-weight:900;">{}</span>', obj.order.get_status_display())
        elif obj.order.status == 'shipped':
             return format_html('<span style="color:#215ee1; font-weight:900;">{}</span>', obj.order.get_status_display())
        elif obj.order.status == 'checking':
             return format_html('<span style="color:#ff7623; font-weight:900;">{}</span>', obj.order.get_status_display())
        else: # status = pending
            return format_html('<span style="color:#e1d221; font-weight:900;">{}</span>', obj.order.get_status_display())
    status.short_description = 'حالة الطلب'   
    
    def has_add_permission(self, request):
        return False  # يمنع إضافة كائنات جديدة من لوحة الإدارة

admin.site.register(Order, MyOrdersAdmin)
admin.site.register(OrderDealing, DealingAdmin)