from django.contrib import admin
from store.models import *
from django.utils.html import mark_safe
from store.forms import ProductVariantsForm

class AdsSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'show', 'ad_image')
    search_fields = ('title', 'show')
    list_filter = ('show',)
    
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'brand_image')
    search_fields = ('title', 'featured')
    list_filter = ('featured',)
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured', 'status', 'category_image',)
    search_fields = ('name', 'featured', 'status',)
    list_filter = ('featured', 'status',)
     
class ProductImagesInline(admin.TabularInline): 
    model = ProductImages
    extra = 1
    fields = ('image',)
    
class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    fields = ('name', 'image')
    
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ('size_value',)

class ProductVariantsAdmin(admin.ModelAdmin):
    form = ProductVariantsForm
    list_display = ('product__pid', 'product', 'color', 'size', 'stock', 'reserved', 'sold')
    search_fields = ('product__pid', 'product__name')
    list_filter = ('product', 'product__category', 'product__brand', 'product__featured', 'product__gender_category', 'product__payment_type',)
    exclude = ('reserved', 'sold')

class ProductVariantsInline(admin.TabularInline):
    model = ProductVariants
    extra = 1
    fields = ('size', 'color', 'stock')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_thumbnail', 'sku', 'name', 'category', 'brand', 'ready_to_sale')
    search_fields = ('name', )
    list_filter = ('category', 'gender_category', 'brand', 'ready_to_sale', 'payment_type', 'price', 'point_price', 'tags', 'featured')
    ordering = ('updated_at',)
    inlines = [ProductImagesInline, ProductColorInline, ProductSizeInline, ProductVariantsInline]

admin.site.register(AdsSlider, AdsSliderAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariants, ProductVariantsAdmin)
admin.site.register(Category, CategoryAdmin)