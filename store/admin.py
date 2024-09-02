from django.contrib import admin
from store.models import *
from django.utils.html import mark_safe

class AdsSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'show', 'ad_image')
    search_fields = ('title', 'show')
    list_filter = ('show',)
    
class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'brand_image')
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
    list_display = ('name', 'featured', 'status', 'size_category', 'parent_category', 'category_image')
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
    list_display = ('product_thumbnail' ,'product_item' ,'size', 'stock', 'reserved', 'sold',)
    search_fields = ('product_item',)
    list_filter = ('stock', 'sold', 'reserved')

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    fields = ('name', 'image')

class ProductItemInline(admin.StackedInline):
    model = ProductItem
    extra = 1
    fields = ('sku', 'color')  # إذا كنت ترغب في إضافة ألوان مباشرة هنا، يمكنك إضافة تلك الحقول التي تحتاجها
 
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('sku', 'product__name', 'color', )
    search_fields = ('sku',)
    list_filter = ('sku', 'color')
    inlines = (ProductColorInline,)
   
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_thumbnail', 'name', 'category', 'brand', 'ready_to_sale', 'offer')
    search_fields = ('name', )
    list_filter = ('category', 'brand', 'ready_to_sale', 'payment_type', 'price', 'point_price', 'featured' , 'offer')
    ordering = ('updated_at',)   
    inlines = (ProductImagesInline, ProductItemInline, )


 
admin.site.register(AdsSlider, AdsSliderAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(SizeCategory, SizeCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)

 
 
 
 
 
 

# class ProductVariantsAdmin(admin.ModelAdmin):
#     form = ProductVariantsForm
#     list_display = ('product__pid', 'product', 'color', 'size', 'stock', 'reserved', 'sold')
#     search_fields = ('product__pid', 'product__name')
#     list_filter = ('product', 'product__category', 'product__brand', 'product__featured', 'product__gender_category', 'product__payment_type',)
#     exclude = ('reserved', 'sold')

# class ProductVariantsInline(admin.TabularInline):
#     model = ProductVariants
#     extra = 1
#     fields = ('size', 'color', 'stock')

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('product_thumbnail', 'sku', 'name', 'category', 'brand', 'ready_to_sale')
#     search_fields = ('name', )
#     list_filter = ('category', 'gender_category', 'brand', 'ready_to_sale', 'payment_type', 'price', 'point_price', 'tags', 'featured')
#     ordering = ('updated_at',)
#     inlines = [ProductImagesInline, ProductColorInline, ProductSizeInline, ProductVariantsInline]
