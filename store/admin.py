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

class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    list_filter = ('name',)

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
    readonly_fields = ('sold',)

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1
    fields = ('size', 'stock', ) 
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "size":
            obj_id = request.resolver_match.kwargs.get('object_id')  # الحصول على ID العنصر في التعديل
            if obj_id:
                from .models import ProductItem  # استيراد النموذج هنا لمنع الدوران
                product_item = ProductItem.objects.filter(id=obj_id).first()
                if product_item and product_item.product.category.size_category:
                    kwargs["queryset"] = SizeOption.objects.filter(size_category=product_item.product.category.size_category)
                else:
                    kwargs["queryset"] = SizeOption.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
      
class ProductItemInline(admin.TabularInline):
    model = ProductItem
    extra = 1
    fields = ('sku', 'color', 'image') 

class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('sku', 'product__name', 'color', 'item_image')
    search_fields = ('sku',)
    list_filter = ('sku', 'color')
    inlines = (ProductVariationInline,)
   
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_thumbnail', 'name', 'category', 'brand', 'total_sales', 'available', 'ready_to_sale', 'offer', "interested_count")
    readonly_fields =('total_sales', 'interested_count', 'available',)
    search_fields = ('name', )
    list_filter = ('category', 'brand', 'ready_to_sale', 'featured' , 'offer', 'available',)
    ordering = ('updated_at',)
    inlines = (ProductImagesInline, ProductItemInline,)
    
    def interested_count(self, obj):
        return Interested.objects.filter(product=obj).count()
    interested_count.short_description = "عدد المهتمين"

class InterestedAdmin(admin.ModelAdmin):
    list_display = ('product_thumbnail', 'product', "user", 'created_at')
    readonly_fields =("user", 'product', 'interested_count', 'created_at',)
    search_fields = ('product__name',)
    list_filter = ("user", 'product',)
    
    def interested_count(self, obj):
        return Interested.objects.filter(product=obj.product).count()
    interested_count.short_description = "عدد المهتمين"
    def has_add_permission(self, request):
        return False

admin.site.register(AdsSlider, AdsSliderAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(SizeCategory, SizeCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Interested, InterestedAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)