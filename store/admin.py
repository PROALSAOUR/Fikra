from django.contrib import admin
from store.models import *
from django.utils.html import mark_safe

class AdsProductsInline(admin.TabularInline):
    model = AdsProducts
    extra = 1 
    fields = ('product',)

class AdsSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'show', 'ads_for','ad_image')
    search_fields = ('title', 'show')
    list_filter = ('show',)
    inlines = (AdsProductsInline,)
    
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'products_count', 'brand_image')
    search_fields = ('title', 'featured')
    list_filter = ('featured',)
 
class SizeOptionInline(admin.TabularInline):
    model = SizeOption
    extra = 1 
    fields = ('value',)
 
class SizeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    inlines = (SizeOptionInline ,)
 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'featured', 'status', 'parent_category', 'products_count', 'category_image')
    search_fields = ('name',)
    list_filter = ('featured', 'status', 'size_category', 'parent_category',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_count')
    search_fields = ('name',)
  
class ProductImagesInline(admin.TabularInline): 
    model = ProductImages
    extra = 1
    fields = ('image',)
     
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('item_thumbnail' ,'product_item' ,'size', 'stock', 'sold',)
    search_fields = ('product_item',)
    exclude = ('sold',)
      
class ProductItemInline(admin.TabularInline):
    model = ProductItem
    extra = 1
    fields = ('sku', 'color', 'image') 

class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('sku', 'product__name', 'color', 'item_image')
    search_fields = ('sku',)
    list_filter = ('sku', 'color')
   
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_thumbnail', 'name', 'category', 'brand', 'ready_to_sale', 'offer')
    search_fields = ('name', )
    list_filter = ('category', 'brand', 'ready_to_sale', 'price', 'featured' , 'offer')
    ordering = ('updated_at',)   
    inlines = (ProductImagesInline, ProductItemInline,)

class CoponAdmin(admin.ModelAdmin):
    list_display = ('copon_image', 'name', 'get_value_display', 'min_bill_price', 'price', 'sales_count', 'expiration', 'is_active',)
    search_fields = ('name','value',)
    list_filter = ('is_active',)
    ordering = ('sales_count',)   
    exclude = ('sales_count',)
    
    def get_value_display(self, obj):
        return f"{obj.value}%"
    get_value_display.short_description = 'value' # عنوان العمود في الواجهة
    
class CoponUsageAdmin(admin.ModelAdmin):
    list_display = ('get_gift_image', 'copon_code__name', 'user','sell_price', 'get_now_price', 'has_used', 'purchase_date',)
    search_fields = ('name','value',)
    list_filter = ('has_used','user',)
    ordering = ('purchase_date',)   
    exclude = ('has_used',)
    
    def get_gift_image(self, obj):
        return f"{obj.copon_code.copon_image()}"
    get_gift_image.short_description = 'image' # عنوان العمود في الواجهة
    
    def get_now_price(self, obj):
        return f"{obj.copon_code.price}"
    get_now_price.short_description = 'Current price' # عنوان العمود في الواجهة

class GiftAdmin(admin.ModelAdmin):
    list_display = ('gift_image', 'name', 'get_value_display', 'price', 'sales_count', 'is_active',)
    search_fields = ('name','value',)
    list_filter = ('is_active',)
    ordering = ('sales_count',)   
    exclude = ('sales_count',)
    
    def get_value_display(self, obj):
        return f"{obj.value}"
    get_value_display.short_description = 'value' # عنوان العمود في الواجهة

class GiftItemAdmin(admin.ModelAdmin):
    list_display = ('get_gift_image', 'gift__name', 'buyer', 'recipient', 'sell_price', 'get_now_price', 'has_used', 'purchase_date',)
    search_fields = ('gift__name','buyer',)
    list_filter = ('has_used',)
    ordering = ('purchase_date',)   
    exclude = ('has_used', 'sell_price')
    
    
    def get_gift_image(self, obj):
        return f"{obj.gift.gift_image()}"
    get_gift_image.short_description = 'gift image' # عنوان العمود في الواجهة
    
    def get_now_price(self, obj):
        return f"{obj.gift.price}"
    get_now_price.short_description = 'now price' # عنوان العمود في الواجهة

class GiftDealingAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver_name', 'receiver_phone', 'is_dealt', 'created_at', 'updated_at',)
    search_fields = ('sender',)
    list_filter = ('is_dealt',)
    ordering = ('created_at',)   
    exclude = ('sender', 'receiver_name', 'receiver_phone',)

admin.site.register(AdsSlider, AdsSliderAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(SizeCategory, SizeCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
admin.site.register(Copon, CoponAdmin)
admin.site.register(CoponUsage, CoponUsageAdmin)
admin.site.register(Gift, GiftAdmin)
admin.site.register(GiftItem, GiftItemAdmin)
admin.site.register(GiftDealing, GiftDealingAdmin)