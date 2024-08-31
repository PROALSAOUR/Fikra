from django.contrib import admin
from store.models import *
from django.utils.html import mark_safe
# Register your models here.


class AdsSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'show', 'ad_image')
    search_fields = ('title', 'show')
    
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'brand_image')
    search_fields = ('title', 'featured')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured', 'category_image')
    search_fields = ('name', 'featured')
   
class ProductImagesInline(admin.TabularInline): 
    model = ProductImages
    extra = 1  # عدد النماذج الفارغة التي سيتم عرضها بشكل افتراضي
    fields = ('image',)  # الحقول التي تريد عرضها في واجهة الإدارة
    
class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    fields = ('name', 'image')
    
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ('size_value',)
    
class ProductVariantsAdmin(admin.ModelAdmin):
    list_display = ('product__pid', 'product', 'color', 'size', 'stock', 'reserved', 'sold')
    search_fields = ('product__pid', 'product__name')
    exclude = ('reserved', 'sold')
    
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'product_thumbnail', 'name', 'category', 'brand', 'ready_to_sale')
    search_fields = ('name', 'category', 'gender_category', 'brand', 'ready_to_sale')
    list_filter = ('name',)
    ordering = ('updated_at',)
    inlines = [ProductImagesInline, ProductColorInline, ProductSizeInline]

admin.site.register(AdsSlider, AdsSliderAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariants, ProductVariantsAdmin)
