from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from accounts.models import User
import string

# ======================== Product ======================================

class AdsSlider(models.Model):
    
    ads_options = [
        ('category', 'اعلان لتصنيف'),
        ('one_product', 'اعلان لمنتج معين'),
        ('special_products', 'اعلان لعدة منتجات خاصة'),
        ('just_show', 'منظر فقط'),
    ]
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    img = models.ImageField( upload_to='store/Ads')
    show = models.BooleanField( default=False)
    info = models.TextField(null=True, blank=True)
    ads_for = models.CharField(choices=ads_options, max_length=20, default='special_products')
    category = models.ForeignKey('Category', null=True, blank=True, related_name='ads', on_delete=models.CASCADE)
    one_product = models.ForeignKey('Product', null=True, blank=True, related_name='ads', on_delete=models.CASCADE)
    
    def get_ad_url(self):
        if self.ads_for == 'category':
            return reverse('store:category', kwargs={'slug': self.category.slug})
        elif self.ads_for == 'one_product':
            return reverse('store:product_details', kwargs={'pid': self.one_product.id})
        elif self.ads_for == 'special_products':
            return reverse('store:ad_details', kwargs={'slug': self.slug})
        else:
            return reverse('store:home')
    
    def clean(self):
        super().clean() 

        if self.ads_for == 'category' and not self.category:
            raise ValidationError('Category Ads must be linked to a Category.')
        elif self.ads_for == 'one_product' and not self.one_product:
            raise ValidationError('One Product Ads must be linked to a Product.')

    def ad_image(self):
        return mark_safe("<img src='%s' width='80' height='50'/>" % (self.img.url) )
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'الاعلانات'
    
class AdsProducts(models.Model):
    product =  models.ManyToManyField('Product', related_name='products') 
    Ads_name = models.ForeignKey(AdsSlider, null=True, blank=True, related_name='adsproducts', on_delete=models.CASCADE)
   
class Brand(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField( upload_to='store/Brands')
    featured = models.BooleanField(default=False)
        
    def __str__(self) -> str:
        return self.title
    
    def brand_image(self):
        return mark_safe("<img src='%s' width='50' height='50'/>" % (self.img.url) )
    
    def products_count(self):
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
        ('visible', 'ظاهر'),
        ('hiddin', 'مخفي'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
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
    
    def products_count(self):
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
    price = models.IntegerField(default=0) 
    new_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    bonus =  models.IntegerField(blank=True, null=True, default=20)
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
            return round(discount_percentage, 1)
        return 0

    def get_price(self):
        """تعيد السعر المنتج وفقا لحالة التخفيض """
        if self.offer :
            return self.new_price
        else:
            return self.price
            
    def get_total_stock(self):
        """
        تستعمل هذه الدالة للتحقق من ان المنتج متاح بالمخزن والا فبدلا من عرض السعر في بطاقة المنتج سيتم عرض نفذت الكمية
        """
        total_stock = 0
        for item in self.items.all():
            for variation in item.variations.all():
                total_stock += variation.stock
        return total_stock
    
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

    def sell(self, quantity):
       pass
    
    @property
    def item_thumbnail(self):
        return self.product_item.item_image # استرجع صورة المصغرة من المنتج

    class Meta:
        verbose_name = 'المخزون'
        verbose_name_plural = 'المخزون'
        
# ========================== Favourite ===================================

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    products = models.ManyToManyField(Product)
    
    def __str__(self):
        return f"{self.user.phone_number}قائمة المفضلة الخاصة ب"
    
# ============================= Order ====================================

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    
    def __str__(self) -> str:
        return f'سلة : {self.user.first_name} {self.user.last_name}'
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    cart_item = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='cart_variations')
    qty = models.PositiveIntegerField(default=1)
    
    def get_stock_quantity(self):
        """
        تعيد الكمية المتاحة في المخزون بناءً على الكمية المطلوبة.
        إذا كانت الكمية المطلوبة أكبر من المخزون المتاح، تعيد 0.
        """
        available_stock = self.cart_item.stock
        return max(0, available_stock - self.qty)
    
    def update_qty(self, new_qty):
        if new_qty < 1:
            raise ValueError("الكمية يجب أن تكون أكبر من 0.")
        if new_qty > self.cart_item.stock:
            raise ValueError("الكمية المطلوبة أكبر من المخزون المتاح.")
        self.qty = new_qty
        self.save()
        
class Order(models.Model):
    
    ORDER_STATUS = [
        ('pending', 'جاري المعالجة'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التسليم'),
        ('canceled', 'تم الإلغاء'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    total_price = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    order_item = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='order_items')
    qty = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()




