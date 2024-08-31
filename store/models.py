from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
import string


class AdsSlider(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField( upload_to='store/Ads')
    show = models.BooleanField( default=False)
    
    # url_type = models.CharField(max_length=20, choices=[
    #     ('product', 'Product'),
    #     ('category', 'Category'),
    #     ('custom', 'Custom Page'),
    # ], default='custom') 
    # url_value = models.CharField(max_length=255, blank=True, null=True) #  قيمة مختلفة بناءً على نوع الرابط
    
    # def get_ad_url(self):
    #     if self.url_type == 'product':
    #         return reverse('product_detail', args=[self.url_value])
    #     elif self.url_type == 'category':
    #         return reverse('category_detail', args=[self.url_value])  # Assuming 'category_detail' is the URL name for category
    #     else:
    #         return self.url_value  # Custom URL       
    # def ad_image(self):
    #     url = self.get_ad_url()
    #     return mark_safe("<img src='%s' width='80' height='50'/>" % (url, self.img.url) )
    def ad_image(self):
        return mark_safe("<img src='%s' width='80' height='50'/>" % (self.img.url) )
    
    def __str__(self) -> str:
        return self.title
    
class Brand(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField( upload_to='store/Brands')
    featured = models.BooleanField(default=False)
        
    def __str__(self) -> str:
        return self.title
    
    def brand_image(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.img.url) )
    
    class Meta:
        verbose_name_plural = 'Brands'
  
class Category(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField( upload_to='store/categories')  
    featured = models.BooleanField(default=False)
    
    def category_image(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.img.url) )
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Tag(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Tags'

class ProductImages(models.Model):
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/Products/images')
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name_plural = 'Product Images'

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=12, max_length=30, prefix='pr', alphabet= string.ascii_lowercase + string.digits)
    sku = ShortUUIDField(unique=True, length=8, max_length=20, alphabet= string.ascii_lowercase + string.digits)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category =  models.ForeignKey(Category ,related_name='products', on_delete=models.SET_NULL, blank=True, null=True)
    brand = models.ForeignKey(Brand, related_name='products' , on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True) 
    gender_category = models.CharField(
        max_length=10, 
        choices=[ 
            ('male', 'رجالي'),
            ('female', 'نسائي'),
            ('unisex', 'صالح للجنسين'),
            ], 
        default='unisex')
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
    price = models.IntegerField() 
    new_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    point_price = models.IntegerField(blank=True, null=True)
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

class ProductColor(models.Model):
    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='store/Products/product_colors/')
    
    def __str__(self):
        return self.name
    
    def product_color(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.image.url) )

class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    size_value = models.CharField(max_length=10)
    
    def __str__(self):
        return  self.size_value

class ProductVariants(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, related_name='variants', on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, related_name='variants', on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)  # الكمية المتاحة
    reserved = models.IntegerField(default=0)  # الكمية المحجوزة
    sold = models.IntegerField(default=0)  # الكمية المباعة
    
    def __str__(self):
        return f"{self.product.name} - {self.color.name} - {self.size}"
    
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
    
    class Meta:
        verbose_name_plural = 'Product Variants'