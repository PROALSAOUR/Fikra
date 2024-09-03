from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
import string

# ======================== Product ======================================

class AdsSlider(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField( upload_to='store/Ads')
    show = models.BooleanField( default=False)
    
    def ad_image(self):
        return mark_safe("<img src='%s' width='80' height='50'/>" % (self.img.url) )
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'الاعلانات'
    
class Brand(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField( upload_to='store/Brands')
    featured = models.BooleanField(default=False)
        
    def __str__(self) -> str:
        return self.title
    
    def brand_image(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.img.url) )
    
    def brand_count(self):
        return self.products.count()
    
    class Meta:
        verbose_name = 'علامة تجارية'
        verbose_name_plural = 'العلامات تجارية'

class SizeCategory(models.Model):
    name = models.CharField(max_length=80)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'فئة المقاسات'
        verbose_name_plural = 'فئات المقاسات'

class SizeOption(models.Model):
    value = models.CharField(max_length=20)
    size_category = models.ForeignKey(SizeCategory, on_delete=models.CASCADE, related_name='size_options')
    
    def __str__(self) -> str:
        return self.value
    
    class Meta:
        verbose_name = 'مقاس'
        verbose_name_plural = 'المقاسات'

class Category(models.Model):
    status_choices = [
        ('visible', 'Visible'),
        ('hiddin', 'Hiddin'),
    ]
    
    name = models.CharField(max_length=100)
    img = models.ImageField( upload_to='store/categories') 
    gender_cat = models.BooleanField(default=False) 
    featured = models.BooleanField(default=False)
    status = models.CharField(choices=status_choices, max_length=20, default='visible')
    size_category = models.ForeignKey(SizeCategory, on_delete=models.CASCADE, null=True, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE,  null=True, blank=True)
    
    def category_image(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.img.url) )
    
    def __str__(self) -> str:
        return self.name
    
    def category_count(self):
        return self.products.count()
    
    class Meta:
        verbose_name = 'تصنيف'
        verbose_name_plural = 'التصنيفات'

class Tag(models.Model):
    name = models.CharField(max_length=20, blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    def tag_count(self):
        return self.products.count()
    
    class Meta:
        verbose_name = 'هاشتاج'
        verbose_name_plural = 'هاشتاج'

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=12, max_length=30, prefix='pr', alphabet= string.ascii_lowercase + string.digits)
    name = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, related_name='products')
    thumbnail_img = models.ImageField(upload_to='store/Products/thumbnails')
    featured = models.BooleanField(default=False)   
    payment_type = models.CharField(
        max_length=10,
        choices=[
            ('money', 'نقود'),
            ('points', 'نقاط'),
        ],
        default='money'
    )
    price = models.IntegerField(default=0) 
    new_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    point_price = models.IntegerField(blank=True, null=True)
    offer = models.BooleanField(default=False)
    ready_to_sale = models.BooleanField(default=False)
    upload_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     

    def __str__(self) -> str:
        return self.name
    
    def product_thumbnail(self):
        # دالة مسؤولة عن عرض صورة المنتج المصغرة في لوحة الادارة
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.thumbnail_img.url) )
    
    def get_offer_percentage(self):
        if self.new_price and self.new_price < self.price:
            discount_percentage = ((self.price - self.new_price) / self.price) * 100
            return round(discount_percentage, 2)
        return 0

    def update_offer_status(self):
        """
        Update the offer status based on the presence of a new price.
        """
        if self.new_price and self.new_price < self.price:
            self.offer = True
        else:
            self.offer = False
        self.save()
        
    class Meta:
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'

class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/Products/images')
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name = 'صورة المنتج'
        verbose_name_plural = 'صور المنتج'

class ProductItem(models.Model):
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    sku = ShortUUIDField(unique=True, prefix='sku',  length=8, max_length=20, alphabet= string.ascii_lowercase + string.digits)
    color =  models.CharField(max_length=255)
    image = models.ImageField(upload_to='store/Products/product_items/', null=True)
    
    def item_image(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.image.url) )

    def __str__(self) -> str:
        return str(self.sku)
    
    class Meta:
        verbose_name = 'متغير المنتج'
        verbose_name_plural = 'متغيرات المنتج'

class ProductVariation(models.Model):
    product_item = models.ForeignKey(ProductItem, related_name='variations', on_delete=models.PROTECT,)
    size = models.ForeignKey(SizeOption, related_name='variations', on_delete=models.PROTECT)
    stock = models.IntegerField(default=0)  # الكمية المتاحة
    reserved = models.IntegerField(default=0)  # الكمية المحجوزة
    sold = models.IntegerField(default=0)  # الكمية المباعة

    def __str__(self):
        return f"{self.product_item} - {self.product_item.product.name} - {self.product_item.color} - {self.size}"

    def update_stock(self, quantity_change):
        """
        This method updates the stock and ensures the stock never goes negative.
        """
        if self.stock + quantity_change >= 0:
            self.stock += quantity_change
            self.save()
        else:
            raise ValueError("مخزون غير كاف!")

    def reserve_stock(self, quantity):
        """
        Reserve stock when an item is added to a cart.
        """
        if self.stock >= quantity:
            self.stock -= quantity
            self.reserved += quantity
            self.save()
        else:
            raise ValueError("لا يوجد مخزون كاف متاح للحجز.")

    def sell(self, quantity):
        """
        Confirm the sale of reserved stock.
        """
        if self.reserved >= quantity:
            self.reserved -= quantity
            self.sold += quantity
            self.save()
        else:
            raise ValueError("Not enough reserved stock to sell.")

    @property
    def item_thumbnail(self):
        return self.product_item.item_image # استرجع صورة المصغرة من المنتج

    class Meta:
        verbose_name = 'المخزون'
        verbose_name_plural = 'المخزون'
        
# ========================== Favourite ===================================

# ============================= Order ====================================
