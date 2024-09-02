from django.contrib import admin
from store.models import *
from django.utils.html import mark_safe

class AdsSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'show', 'ad_image')
    search_fields = ('title', 'show')
    list_filter = ('show',)
    
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'brand_count', 'brand_image')
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
    list_display = ('name', 'featured', 'status', 'parent_category', 'category_count', 'category_image')
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
    list_display = ('item_thumbnail' ,'product_item' ,'size', 'stock', 'reserved', 'sold',)
    search_fields = ('product_item',)
    exclude = ('reserved', 'sold',)
      
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
    list_filter = ('category', 'brand', 'ready_to_sale', 'payment_type', 'price', 'point_price', 'featured' , 'offer')
    ordering = ('updated_at',)   
    inlines = (ProductImagesInline, ProductItemInline,)

admin.site.register(AdsSlider, AdsSliderAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(SizeCategory, SizeCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)